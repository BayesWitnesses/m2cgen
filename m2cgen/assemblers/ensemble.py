from m2cgen import ast
from m2cgen.assemblers import utils
from m2cgen.assemblers.base import ModelAssembler
from m2cgen.assemblers import TreeModelAssembler


class RandomForestModelAssembler(ModelAssembler):

    def assemble(self):
        trees = self.model.estimators_

        def assemble_tree_expr(t):
            assembler = TreeModelAssembler(t)

            return ast.SubroutineExpr(assembler.assemble())

        assembled_trees = [assemble_tree_expr(t) for t in trees]
        return utils.apply_bin_op(
            utils.apply_op_to_expressions(ast.BinNumOpType.ADD,
                                          *assembled_trees),
            ast.NumVal(1 / self.model.n_estimators),
            ast.BinNumOpType.MUL)
