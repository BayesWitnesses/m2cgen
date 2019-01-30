from m2cgen import ast
from m2cgen.assemblers import utils
from m2cgen.assemblers.base import ModelAssembler


class LinearModelAssembler(ModelAssembler):

    def assemble(self):
        return self._build_ast()

    def _build_ast(self):
        coef = utils.to_2d_array(self.model.coef_)
        intercept = utils.to_1d_array(self.model.intercept_)

        if coef.shape[0] == 1:
            return _linear_to_ast(coef[0], intercept[0])

        exprs = []
        for idx in range(coef.shape[0]):
            exprs.append(ast.SubroutineExpr(
                _linear_to_ast(coef[idx], intercept[idx])))
        return ast.VectorVal(exprs)


def _linear_to_ast(coef, intercept):
    feature_weight_mul_ops = []

    for index, value in enumerate(coef):
        feature_weight_mul_ops.append(
            utils.mul(ast.FeatureRef(index), ast.NumVal(value)))

    return utils.apply_op_to_expressions(
        ast.BinNumOpType.ADD,
        ast.NumVal(intercept),
        *feature_weight_mul_ops)
