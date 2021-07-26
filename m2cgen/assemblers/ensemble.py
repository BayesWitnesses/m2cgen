from m2cgen import assemblers, ast


class RandomForestModelAssembler(assemblers.base.ModelAssembler):

    def assemble(self):
        trees = self.model.estimators_

        def assemble_tree_expr(t):
            assembler = assemblers.TreeModelAssembler(t)

            return assembler.assemble()

        assembled_trees = [assemble_tree_expr(t) for t in trees]
        return assemblers.utils.apply_bin_op(
            assemblers.utils.apply_op_to_expressions(ast.BinNumOpType.ADD, *assembled_trees),
            ast.NumVal(1 / self.model.n_estimators),
            ast.BinNumOpType.MUL)
