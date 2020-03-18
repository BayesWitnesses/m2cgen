import numpy as np

from m2cgen import ast
from m2cgen.assemblers import utils
from m2cgen.assemblers.base import ModelAssembler


class BaseLinearModelAssembler(ModelAssembler):

    def assemble(self):
        return self._build_ast()

    def _build_ast(self):
        coef = utils.to_2d_array(self._get_coef())
        intercept = utils.to_1d_array(self._get_intercept())

        if coef.shape[0] == 1:
            return _linear_to_ast(coef[0], intercept[0])

        exprs = []
        for idx in range(coef.shape[0]):
            exprs.append(_linear_to_ast(coef[idx], intercept[idx]))
        return ast.VectorVal(exprs)

    def _get_intercept(self):
        raise NotImplementedError

    def _get_coef(self):
        raise NotImplementedError


class SklearnLinearModelAssembler(BaseLinearModelAssembler):

    def _get_intercept(self):
        return getattr(self.model, "intercept_",
                       np.zeros(self._get_coef().shape[0]))

    def _get_coef(self):
        return self.model.coef_


class StatsmodelsLinearModelAssembler(BaseLinearModelAssembler):

    def __init__(self, model):
        super(StatsmodelsLinearModelAssembler, self).__init__(model)
        const_idx = self.model.model.data.const_idx
        if const_idx is None and self.model.k_constant:
            raise ValueError("Unknown constant position")
        self.const_idx = const_idx

    def _get_intercept(self):
        return (self.model.params[self.const_idx]
                if self.model.k_constant
                else 0.0)

    def _get_coef(self):
        idxs = np.arange(len(self.model.params))
        return (
            self.model.params[idxs != self.const_idx]
            if self.model.k_constant
            else self.model.params)


class ProcessMLEModelAssembler(BaseLinearModelAssembler):

    def _get_intercept(self):
        return 0.0

    def _get_coef(self):
        return self.model.params[:self.model.k_exog]


def _linear_to_ast(coef, intercept):
    feature_weight_mul_ops = []

    for index, value in enumerate(coef):
        feature_weight_mul_ops.append(
            utils.mul(ast.FeatureRef(index), ast.NumVal(value)))

    return utils.apply_op_to_expressions(
        ast.BinNumOpType.ADD,
        ast.NumVal(intercept),
        *feature_weight_mul_ops)
