import json
import numpy as np
from m2cgen import ast
from m2cgen.assemblers import utils
from m2cgen.assemblers.base import ModelAssembler


class BaseBoostingAssembler(ModelAssembler):

    classifier_name = None

    def __init__(self, model, trees, base_score=0, tree_limit=None):
        super().__init__(model)
        self.all_trees = trees
        self._base_score = base_score

        self._output_size = 1
        self._is_classification = False

        assert tree_limit is None or tree_limit > 0, "Unexpected tree limit"
        self._tree_limit = tree_limit

        model_class_name = type(model).__name__
        if model_class_name == self.classifier_name:
            self._is_classification = True
            if model.n_classes_ > 2:
                self._output_size = model.n_classes_

    def assemble(self):
        if self._is_classification:
            if self._output_size == 1:
                return self._assemble_bin_class_output(self.all_trees)
            else:
                return self._assemble_multi_class_output(self.all_trees)
        else:
            return self._assemble_single_output(
                self.all_trees, self._base_score)

    def _assemble_single_output(self, trees, base_score=0):
        if self._tree_limit:
            trees = trees[:self._tree_limit]

        trees_ast = [self._assemble_tree(t) for t in trees]
        result_ast = utils.apply_op_to_expressions(
            ast.BinNumOpType.ADD,
            ast.NumVal(base_score),
            *trees_ast)
        return ast.SubroutineExpr(result_ast)

    def _assemble_multi_class_output(self, trees):
        # Multi-class output is calculated based on discussion in
        # https://github.com/dmlc/xgboost/issues/1746#issuecomment-295962863
        splits = _split_trees_by_classes(trees, self._output_size)

        base_score = self._base_score
        exprs = [self._assemble_single_output(t, base_score) for t in splits]

        proba_exprs = utils.softmax_exprs(exprs)
        return ast.VectorVal(proba_exprs)

    def _assemble_bin_class_output(self, trees):
        # Base score is calculated based on https://github.com/dmlc/xgboost/blob/master/src/objective/regression_loss.h#L64  # noqa
        # return -logf(1.0f / base_score - 1.0f);
        base_score = 0
        if self._base_score != 0:
            base_score = -np.log(1.0 / self._base_score - 1.0)

        expr = self._assemble_single_output(trees, base_score)

        proba_expr = utils.sigmoid_expr(expr, to_reuse=True)

        return ast.VectorVal([
            ast.BinNumExpr(ast.NumVal(1), proba_expr, ast.BinNumOpType.SUB),
            proba_expr
        ])

    def _assemble_tree(self, tree):
        raise NotImplementedError


class XGBoostModelAssembler(BaseBoostingAssembler):

    classifier_name = "XGBClassifier"

    def __init__(self, model):
        feature_names = model.get_booster().feature_names
        self._feature_name_to_idx = {
            name: idx for idx, name in enumerate(feature_names)
        }

        model_dump = model.get_booster().get_dump(dump_format="json")
        trees = [json.loads(d) for d in model_dump]

        # Limit the number of trees that should be used for
        # assembling (if applicable).
        best_ntree_limit = getattr(model, "best_ntree_limit", None)

        super().__init__(model, trees, base_score=model.base_score,
                         tree_limit=best_ntree_limit)

    def _assemble_tree(self, tree):
        if "leaf" in tree:
            return ast.NumVal(tree["leaf"])

        threshold = ast.NumVal(tree["split_condition"])
        feature_idx = self._feature_name_to_idx[tree["split"]]
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


class LightGBMModelAssembler(BaseBoostingAssembler):

    classifier_name = "LGBMClassifier"

    def __init__(self, model):
        model_dump = model.booster_.dump_model()
        trees = [m["tree_structure"] for m in model_dump["tree_info"]]

        super().__init__(model, trees)

    def _assemble_tree(self, tree):
        if "leaf_value" in tree:
            return ast.NumVal(tree["leaf_value"])

        threshold = ast.NumVal(tree["threshold"])
        feature_ref = ast.FeatureRef(tree["split_feature"])

        op = ast.CompOpType.from_str_op(tree["decision_type"])
        assert op == ast.CompOpType.LTE, "Unexpected comparison op"

        # Make sure that if the 'default_left' is true the left tree branch
        # ends up in the "else" branch of the ast.IfExpr.
        if tree['default_left']:
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


def _split_trees_by_classes(trees, n_classes):
    # Splits are computed based on a comment
    # https://github.com/dmlc/xgboost/issues/1746#issuecomment-267400592.
    trees_by_classes = [[] for _ in range(n_classes)]
    for i in range(len(trees)):
        class_idx = i % n_classes
        trees_by_classes[class_idx].append(trees[i])
    return trees_by_classes
