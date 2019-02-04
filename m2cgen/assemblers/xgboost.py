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
        model_class_name = type(model).__name__
        if model_class_name == "XGBClassifier" and self.model.n_classes_ > 2:
            self._output_size = self.model.n_classes_

    def assemble(self):
        model_dump = self.model.get_booster().get_dump(dump_format="json")
        trees = [json.loads(d) for d in model_dump]

        if self._output_size == 1:
            return self._assemble_single_output(trees)
        else:
            split_size = len(trees) / self._output_size
            splits = np.array_split(trees, split_size)
            exprs = [self._assemble_single_output(t) for t in splits]
            return ast.VectorVal(exprs)

    def _assemble_single_output(self, trees):
        trees_ast = [self._assemble_tree(t) for t in trees]
        result_ast = utils.apply_op_to_expressions(
            ast.BinNumOpType.ADD,
            ast.NumVal(self._base_score),
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
        assert False, "Unexpected tree child ID {}".format(child_id)
