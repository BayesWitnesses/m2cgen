from m2cgen.ast import *
from m2cgen.model2ast import utils


class ModelAstConverter:

    def __init__(self, model):
        self.model = model

    def convert_to_ast(self):
        raise NotImplementedError


class LinearRegressionConverter(ModelAstConverter):

    def convert_to_ast(self):
        feature_weight_mul_ops = []

        for (index, value) in enumerate(self.model.coef_):
            feature_weight_mul_ops.append(utils.mul(FeatureRef(index), NumVal(value)))

        return utils.apply_op_to_expressions(
            BinNumOpType.ADD,
            NumVal(self.model.intercept_),
            *feature_weight_mul_ops)
