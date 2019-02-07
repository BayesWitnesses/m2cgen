import json
import numpy as np
from m2cgen import ast
from m2cgen.assemblers import utils
from m2cgen.assemblers.base import ModelAssembler


class XGBoostModelAssembler(ModelAssembler):

    def __init__(self, model):
        super().__init__(model)
        self._base_score = self.model.base_score
        self._n_estimators = self.model.n_estimators

        feature_names = enumerate(self.model.get_booster().feature_names)
        self._feature_name_to_idx = {name: idx for idx, name in feature_names}

        self._output_size = 1
        self._is_classification = False
        model_class_name = type(model).__name__
        if model_class_name == "XGBClassifier":
            self._is_classification = True
            if self.model.n_classes_ > 2:
                self._output_size = self.model.n_classes_

    def assemble(self):
        model_dump = self.model.get_booster().get_dump(dump_format="json")
        trees = [json.loads(d) for d in model_dump]

        if self._is_classification:
            if self._output_size == 1:
                return self._assemble_bin_class_output(trees)
            else:
                return self._assemble_multi_class_output(trees)
        else:
            return self._assemble_single_output(trees, self._base_score)

    def _assemble_multi_class_output(self, trees):
        # Multi-class output is calculated based on discussion in
        # https://github.com/dmlc/xgboost/issues/1746#issuecomment-295962863
        splits = _split_trees_by_classes(trees, self._output_size)

        base_score = self._base_score
        exprs = [self._assemble_single_output(t, base_score) for t in splits]
        exp_exprs = [ast.ExpExpr(e, to_cache=True) for e in exprs]

        exp_sum_expr = ast.BinNumExpr(
            exp_exprs[0],
            utils.apply_op_to_expressions(
                ast.BinNumOpType.ADD, *exp_exprs[1:]),
            ast.BinNumOpType.ADD,
            to_cache=True)

        norm_exprs = [
            ast.BinNumExpr(e, exp_sum_expr, ast.BinNumOpType.DIV)
            for e in exp_exprs
        ]
        return ast.VectorVal(norm_exprs)

    def _assemble_bin_class_output(self, trees):
        # Base score is calculated based on https://github.com/dmlc/xgboost/blob/master/src/objective/regression_loss.h#L64  # noqa
        # return -logf(1.0f / base_score - 1.0f);
        base_score = -np.log(1.0 / self._base_score - 1.0)
        expr = self._assemble_single_output(trees, base_score)

        neg_expr = ast.BinNumExpr(ast.NumVal(0), expr, ast.BinNumOpType.SUB)
        exp_expr = ast.ExpExpr(neg_expr)
        log_loss_expr = ast.BinNumExpr(
            ast.NumVal(1),
            ast.BinNumExpr(ast.NumVal(1), exp_expr, ast.BinNumOpType.ADD),
            ast.BinNumOpType.DIV,
            to_cache=True)

        return ast.VectorVal([
            ast.BinNumExpr(ast.NumVal(1), log_loss_expr, ast.BinNumOpType.SUB),
            log_loss_expr
        ])

    def _assemble_single_output(self, trees, base_score):
        trees_ast = [self._assemble_tree(t) for t in trees]
        result_ast = utils.apply_op_to_expressions(
            ast.BinNumOpType.ADD,
            ast.NumVal(base_score),
            *trees_ast)
        return ast.SubroutineExpr(result_ast)

    def _assemble_tree(self, tree):
        if "leaf" in tree:
            return ast.NumVal(tree["leaf"])

        threshold = ast.NumVal(tree["split_condition"])
        feature_idx = self._feature_name_to_idx[tree["split"]]
        feature_ref = ast.FeatureRef(feature_idx)

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


def _split_trees_by_classes(trees, n_classes):
    # Splits are computed based on a comment
    # https://github.com/dmlc/xgboost/issues/1746#issuecomment-267400592.
    trees_by_classes = [[] for _ in range(n_classes)]
    for i in range(len(trees)):
        class_idx = i % n_classes
        trees_by_classes[class_idx].append(trees[i])
    return trees_by_classes
