from m2cgen.ast import ast
from m2cgen.ast.assemblers import utils
from m2cgen.ast.assemblers.base import ModelAssembler
from m2cgen.ast.assemblers.tree import TreeModelAssembler


class RandomForestModelAssembler(ModelAssembler):
    def __init__(self, model):
        super().__init__(model)

    def assemble(self):
        coef = 1.0 / self.model.n_estimators
        trees = self.model.estimators_

        def assemble_tree_expr(t):
            assembler = TreeModelAssembler(t)
            return ast.BinNumExpr(
                ast.LogicalBlockExpr(assembler.assemble()),
                ast.NumVal(coef),
                ast.BinNumOpType.MUL)

        assembled_trees = [assemble_tree_expr(t) for t in trees]
        return utils.apply_op_to_expressions(
            ast.BinNumOpType.ADD, *assembled_trees)
