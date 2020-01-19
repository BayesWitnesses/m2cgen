import json
import numpy as np
from m2cgen import ast
from m2cgen.assemblers import utils
from m2cgen.assemblers.base import ModelAssembler
from m2cgen.assemblers.linear import _linear_to_ast


LEAVES_CUTOFF_THRESHOLD = 3000


class BaseBoostingAssembler(ModelAssembler):

    classifier_name = None

    def __init__(self, model, estimator_params, base_score=0):
        super().__init__(model)
        self._all_estimator_params = estimator_params
        self._base_score = base_score

        self._output_size = 1
        self._is_classification = False

        model_class_name = type(model).__name__
        if model_class_name == self.classifier_name:
            self._is_classification = True
            if model.n_classes_ > 2:
                self._output_size = model.n_classes_

    def assemble(self):
        if self._is_classification:
            if self._output_size == 1:
                return self._assemble_bin_class_output(
                    self._all_estimator_params)
            else:
                return self._assemble_multi_class_output(
                    self._all_estimator_params)
        else:
            return self._assemble_single_output(
                self._all_estimator_params, base_score=self._base_score)

    def _assemble_single_output(self, estimator_params,
                                base_score=0, class_idx=0):
        estimators_ast = self._assemble_estimators(estimator_params, class_idx)

        tmp_ast = utils.apply_op_to_expressions(
            ast.BinNumOpType.ADD,
            ast.NumVal(base_score),
            *estimators_ast)

        result_ast = self._final_transform(tmp_ast)

        return ast.SubroutineExpr(result_ast)

    def _assemble_multi_class_output(self, estimator_params):
        # Multi-class output is calculated based on discussion in
        # https://github.com/dmlc/xgboost/issues/1746#issuecomment-295962863
        splits = _split_estimators_by_classes(
            estimator_params, self._output_size)

        base_score = self._base_score
        exprs = [
            self._assemble_single_output(e, base_score=base_score, class_idx=i)
            for i, e in enumerate(splits)
        ]

        proba_exprs = utils.softmax_exprs(exprs)
        return ast.VectorVal(proba_exprs)

    def _assemble_bin_class_output(self, estimator_params):
        # Base score is calculated based on https://github.com/dmlc/xgboost/blob/master/src/objective/regression_loss.h#L64  # noqa
        # return -logf(1.0f / base_score - 1.0f);
        base_score = 0
        if self._base_score != 0:
            base_score = -np.log(1.0 / self._base_score - 1.0)

        expr = self._assemble_single_output(
            estimator_params, base_score=base_score)

        proba_expr = utils.sigmoid_expr(expr, to_reuse=True)

        return ast.VectorVal([
            ast.BinNumExpr(ast.NumVal(1), proba_expr, ast.BinNumOpType.SUB),
            proba_expr
        ])

    def _final_transform(self, ast_to_transform):
        return ast_to_transform

    def _assemble_estimators(self, estimator_params, class_idx):
        raise NotImplementedError


class BaseTreeBoostingAssembler(BaseBoostingAssembler):

    def __init__(self, model, trees, base_score=0, tree_limit=None,
                 leaves_cutoff_threshold=LEAVES_CUTOFF_THRESHOLD):
        super().__init__(model, trees, base_score=base_score)
        self._leaves_cutoff_threshold = leaves_cutoff_threshold
        assert tree_limit is None or tree_limit > 0, "Unexpected tree limit"
        self._tree_limit = tree_limit

    def _assemble_estimators(self, trees, class_idx):
        if self._tree_limit:
            trees = trees[:self._tree_limit]

        trees_ast = [ast.SubroutineExpr(self._assemble_tree(t)) for t in trees]

        # In a large tree we need to generate multiple subroutines to avoid
        # java limitations https://github.com/BayesWitnesses/m2cgen/issues/103.
        trees_num_leaves = [self._count_leaves(t) for t in trees]
        if sum(trees_num_leaves) > self._leaves_cutoff_threshold:
            return self._split_into_subroutines(trees_ast, trees_num_leaves)
        else:
            return trees_ast

    def _split_into_subroutines(self, trees_ast, trees_num_leaves):
        result = []
        subroutine_trees = []
        subroutine_sum_leaves = 0
        for tree, num_leaves in zip(trees_ast, trees_num_leaves):
            next_sum = subroutine_sum_leaves + num_leaves
            if subroutine_trees and next_sum > self._leaves_cutoff_threshold:
                # Exceeded the max leaves in the current subroutine,
                # finalize this one and start a new one.
                partial_result = utils.apply_op_to_expressions(
                    ast.BinNumOpType.ADD,
                    *subroutine_trees)

                result.append(ast.SubroutineExpr(partial_result))

                subroutine_trees = []
                subroutine_sum_leaves = 0

            subroutine_sum_leaves += num_leaves
            subroutine_trees.append(tree)

        if subroutine_trees:
            partial_result = utils.apply_op_to_expressions(
                ast.BinNumOpType.ADD,
                *subroutine_trees)
            result.append(ast.SubroutineExpr(partial_result))
        return result

    def _assemble_tree(self, tree):
        raise NotImplementedError

    @staticmethod
    def _count_leaves(trees):
        raise NotImplementedError


class XGBoostTreeModelAssembler(BaseTreeBoostingAssembler):

    classifier_name = "XGBClassifier"

    def __init__(self, model,
                 leaves_cutoff_threshold=LEAVES_CUTOFF_THRESHOLD):
        feature_names = model.get_booster().feature_names
        self._feature_name_to_idx = {
            name: idx for idx, name in enumerate(feature_names or [])
        }

        model_dump = model.get_booster().get_dump(dump_format="json")
        trees = [json.loads(d) for d in model_dump]

        # Limit the number of trees that should be used for
        # assembling (if applicable).
        best_ntree_limit = getattr(model, "best_ntree_limit", None)

        super().__init__(model, trees, base_score=model.base_score,
                         tree_limit=best_ntree_limit,
                         leaves_cutoff_threshold=leaves_cutoff_threshold)

    def _assemble_tree(self, tree):
        if "leaf" in tree:
            return ast.NumVal(tree["leaf"])

        threshold = ast.NumVal(tree["split_condition"])
        split = tree["split"]
        feature_idx = self._feature_name_to_idx.get(split, split)
        feature_ref = ast.FeatureRef(feature_idx)

        # Since comparison with NaN (missing) value always returns false we
        # should make sure that the node ID specified in the "missing" field
        # always ends up in the "else" branch of the ast.IfExpr.
        use_lt_comp = tree["missing"] == tree["no"]
        if use_lt_comp:
            comp_op = ast.CompOpType.LT
            true_child_id = tree["yes"]
            false_child_id = tree["no"]
        else:
            comp_op = ast.CompOpType.GTE
            true_child_id = tree["no"]
            false_child_id = tree["yes"]

        return ast.IfExpr(ast.CompExpr(feature_ref, threshold, comp_op),
                          self._assemble_child_tree(tree, true_child_id),
                          self._assemble_child_tree(tree, false_child_id))

    def _assemble_child_tree(self, tree, child_id):
        for child in tree["children"]:
            if child["nodeid"] == child_id:
                return self._assemble_tree(child)
        assert False, "Unexpected child ID {}".format(child_id)

    @staticmethod
    def _count_leaves(tree):
        queue = [tree]
        num_leaves = 0

        while queue:
            tree = queue.pop()
            if "leaf" in tree:
                num_leaves += 1
            elif "children" in tree:
                for child in tree["children"]:
                    queue.append(child)
        return num_leaves


class XGBoostLinearModelAssembler(BaseBoostingAssembler):

    classifier_name = "XGBClassifier"

    def __init__(self, model):
        model_dump = model.get_booster().get_dump(dump_format="json")
        weights = json.loads(model_dump[0])["weight"]
        self._bias = json.loads(model_dump[0])["bias"]
        super().__init__(model, weights,
                         base_score=model.base_score)

    def _assemble_estimators(self, weights, class_idx):
        coef = utils.to_1d_array(weights)
        return [_linear_to_ast(coef, self._bias[class_idx])]


class XGBoostModelAssemblerSelector(ModelAssembler):

    def __init__(self, model):
        model_dump = model.get_booster().get_dump(dump_format="json")
        if len(model_dump) == 1 and all(i in json.loads(model_dump[0])
                                        for i in ("weight", "bias")):
            self.assembler = XGBoostLinearModelAssembler(model)
        else:
            self.assembler = XGBoostTreeModelAssembler(model)

    def assemble(self):
        return self.assembler.assemble()


class LightGBMModelAssembler(BaseTreeBoostingAssembler):

    classifier_name = "LGBMClassifier"

    def __init__(self, model,
                 leaves_cutoff_threshold=LEAVES_CUTOFF_THRESHOLD):
        model_dump = model.booster_.dump_model()
        trees = [m["tree_structure"] for m in model_dump["tree_info"]]

        self.n_iter = len(trees) // model_dump["num_tree_per_iteration"]
        self.average_output = model_dump.get("average_output", False)

        super().__init__(model, trees,
                         leaves_cutoff_threshold=leaves_cutoff_threshold)

    def _final_transform(self, ast_to_transform):
        if self.average_output:
            coef = 1 / self.n_iter
            return utils.apply_bin_op(
                ast_to_transform,
                ast.NumVal(coef),
                ast.BinNumOpType.MUL)
        else:
            return super()._final_transform(ast_to_transform)

    def _assemble_tree(self, tree):
        if "leaf_value" in tree:
            return ast.NumVal(tree["leaf_value"])

        threshold = ast.NumVal(tree["threshold"])
        feature_ref = ast.FeatureRef(tree["split_feature"])

        op = ast.CompOpType.from_str_op(tree["decision_type"])
        assert op == ast.CompOpType.LTE, "Unexpected comparison op"

        # Make sure that if the "default_left" is true the left tree branch
        # ends up in the "else" branch of the ast.IfExpr.
        if tree["default_left"]:
            op = ast.CompOpType.GT
            true_child = tree["right_child"]
            false_child = tree["left_child"]
        else:
            true_child = tree["left_child"]
            false_child = tree["right_child"]

        return ast.IfExpr(
            ast.CompExpr(feature_ref, threshold, op),
            self._assemble_tree(true_child),
            self._assemble_tree(false_child))

    @staticmethod
    def _count_leaves(tree):
        queue = [tree]
        num_leaves = 0

        while queue:
            tree = queue.pop()
            if "leaf_value" in tree:
                num_leaves += 1
            else:
                queue.append(tree["left_child"])
                queue.append(tree["right_child"])
        return num_leaves


def _split_estimators_by_classes(values, n_classes):
    # Splits are computed based on a comment
    # https://github.com/dmlc/xgboost/issues/1746#issuecomment-267400592.
    estimators_by_classes = [[] for _ in range(n_classes)]
    for i in range(len(values)):
        class_idx = i % n_classes
        estimators_by_classes[class_idx].append(values[i])
    return estimators_by_classes
