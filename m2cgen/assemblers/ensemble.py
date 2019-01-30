from m2cgen import ast
from m2cgen.assemblers import utils
from m2cgen.assemblers.base import ModelAssembler
from m2cgen.assemblers import TreeModelAssembler


class RandomForestModelAssembler(ModelAssembler):

    def assemble(self):
        coef = 1.0 / self.model.n_estimators
        trees = self.model.estimators_

        def assemble_tree_expr(t):
            assembler = TreeModelAssembler(t)

            return utils.apply_bin_op(
                ast.SubroutineExpr(assembler.assemble()),
                ast.NumVal(coef),
                ast.BinNumOpType.MUL)

        assembled_trees = [assemble_tree_expr(t) for t in trees]
        return utils.apply_op_to_expressions(
            ast.BinNumOpType.ADD, *assembled_trees)
