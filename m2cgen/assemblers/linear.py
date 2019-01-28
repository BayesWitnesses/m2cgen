import numpy as np
from m2cgen import ast
from m2cgen.assemblers import utils
from m2cgen.assemblers.base import ModelAssembler


class LinearModelAssembler(ModelAssembler):

    def assemble(self):
        model_ast, is_multi_output = self._build_ast()
        return ast.MainExpr(model_ast, is_multi_output=is_multi_output)

    def _build_ast(self):
        coef = self.model.coef_
        intercept = self.model.intercept_
        if isinstance(coef, np.ndarray) and len(coef.shape) == 2:
            if coef.shape[0] == 1:
                return _linear_to_ast(coef[0], intercept[0]), False
            else:
                exprs = []
                for idx in range(coef.shape[0]):
                    exprs.append(ast.SubroutineExpr(
                        _linear_to_ast(coef[idx], intercept[idx])))
                return ast.ArrayExpr(exprs), True
        else:
            return _linear_to_ast(coef, intercept), False


def _linear_to_ast(coef, intercept):
    feature_weight_mul_ops = []

    for (index, value) in enumerate(coef):
        feature_weight_mul_ops.append(
            utils.mul(ast.FeatureRef(index), ast.NumVal(value)))

    return utils.apply_op_to_expressions(
        ast.BinNumOpType.ADD,
        ast.NumVal(intercept),
        *feature_weight_mul_ops)
