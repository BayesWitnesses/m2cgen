from m2cgen.ast import ast
from m2cgen.ast.assemblers import utils
from m2cgen.ast.assemblers.base import ModelAssembler


class LinearRegressionAssembler(ModelAssembler):

    def assemble(self):
        feature_weight_mul_ops = []

        for (index, value) in enumerate(self.model.coef_):
            feature_weight_mul_ops.append(
                utils.mul(ast.FeatureRef(index), ast.NumVal(value)))

        return utils.apply_op_to_expressions(
            ast.BinNumOpType.ADD,
            ast.NumVal(self.model.intercept_),
            *feature_weight_mul_ops)
