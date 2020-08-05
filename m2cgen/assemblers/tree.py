from m2cgen import ast
from m2cgen.assemblers import utils
from m2cgen.assemblers.base import ModelAssembler


# refer to
# https://github.com/scikit-learn/scikit-learn/blob/fd12d5684ad224ad7760374b1dcca2821c644feb/sklearn/tree/_tree.pyx#L64
TREE_LEAF = -1


class TreeModelAssembler(ModelAssembler):

    def __init__(self, model):
        super().__init__(model)
        self._tree = model.tree_
        self._is_vector_output = False
        if type(self.model).__name__ in {"DecisionTreeClassifier",
                                         "ExtraTreeClassifier"}:
            self._is_vector_output = self.model.n_classes_ > 1

    def assemble(self):
        return self._assemble_node(0)

    def _assemble_node(self, node_id):
        if self._tree.children_left[node_id] == TREE_LEAF:
            return self._assemble_leaf(node_id)
        else:
            return self._assemble_branch(node_id)

    def _assemble_branch(self, node_id):
        left_id = self._tree.children_left[node_id]
        right_id = self._tree.children_right[node_id]
        cond = self._assemble_cond(node_id)
        return ast.IfExpr(cond,
                          self._assemble_node(left_id),
                          self._assemble_node(right_id))

    def _assemble_leaf(self, node_id):
        scores = self._tree.value[node_id][0]
        if self._is_vector_output:
            score_sum = scores.sum() or 1.0
            outputs = [ast.NumVal(s / score_sum) for s in scores]
            return ast.VectorVal(outputs)
        else:
            assert len(scores) == 1, "Unexpected number of outputs"
            return ast.NumVal(scores[0])

    def _assemble_cond(self, node_id):
        feature_idx = self._tree.feature[node_id]
        threshold_num_val = ast.NumVal(self._tree.threshold[node_id])
        return utils.lte(ast.FeatureRef(feature_idx), threshold_num_val)
