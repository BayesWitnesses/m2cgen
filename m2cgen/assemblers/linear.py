import math

import numpy as np

from m2cgen import ast
from m2cgen.assemblers import fallback_expressions, utils
from m2cgen.assemblers.base import ModelAssembler


class BaseLinearModelAssembler(ModelAssembler):

    def assemble(self):
        return self._build_ast()

    def _build_ast(self):
        coef = utils.to_2d_array(self._get_coef())
        intercept = utils.to_1d_array(self._get_intercept())

        if coef.shape[0] == 1:
            return self._final_transform(
                _linear_to_ast(coef[0], intercept[0]))

        exprs = [
            self._final_transform(
                _linear_to_ast(coef[idx], intercept[idx]))
            for idx in range(coef.shape[0])
        ]
        return ast.VectorVal(exprs)

    def _final_transform(self, ast_to_transform):
        return ast_to_transform

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
        super().__init__(model)
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


class GLMMixin:

    def _final_transform(self, ast_to_transform):
        link_function = self._get_link_function_name()
        link_function_lower = link_function.lower()
        supported_inversed_funs = self._get_supported_inversed_funs()
        if link_function_lower not in supported_inversed_funs:
            raise ValueError(
                f"Unsupported link function '{link_function}'")
        fun = supported_inversed_funs[link_function_lower]
        return fun(ast_to_transform)

    def _get_link_function_name(self):
        raise NotImplementedError

    def _get_supported_inversed_funs(self):
        raise NotImplementedError

    def _logit_inversed(self, ast_to_transform):
        return fallback_expressions.sigmoid(ast_to_transform)

    def _power_inversed(self, ast_to_transform):
        power = self._get_power()
        if power == 1:
            return self._identity_inversed(ast_to_transform)
        elif power == -1:
            return self._inverse_power_inversed(ast_to_transform)
        elif power == 2:
            return ast.SqrtExpr(ast_to_transform)
        elif power == -2:
            return self._inverse_squared_inversed(ast_to_transform)
        elif power < 0:  # some languages may not support negative exponent
            return utils.div(
                ast.NumVal(1.0),
                ast.PowExpr(ast_to_transform, ast.NumVal(1 / -power)))
        else:
            return ast.PowExpr(ast_to_transform, ast.NumVal(1 / power))

    def _inverse_power_inversed(self, ast_to_transform):
        return utils.div(ast.NumVal(1.0), ast_to_transform)

    def _sqrt_inversed(self, ast_to_transform):
        return ast.PowExpr(ast_to_transform, ast.NumVal(2.0))

    def _inverse_squared_inversed(self, ast_to_transform):
        return utils.div(ast.NumVal(1.0), ast.SqrtExpr(ast_to_transform))

    def _identity_inversed(self, ast_to_transform):
        return ast_to_transform

    def _log_inversed(self, ast_to_transform):
        return ast.ExpExpr(ast_to_transform)

    def _cloglog_inversed(self, ast_to_transform):
        return utils.sub(
            ast.NumVal(1.0),
            ast.ExpExpr(
                utils.sub(
                    ast.NumVal(0.0),
                    ast.ExpExpr(ast_to_transform))))

    def _negativebinomial_inversed(self, ast_to_transform):
        alpha = self._get_alpha()
        res = utils.sub(
            ast.NumVal(1.0),
            ast.ExpExpr(
                utils.sub(
                    ast.NumVal(0.0),
                    ast_to_transform)))
        return utils.div(
            ast.NumVal(-1.0),
            utils.mul(ast.NumVal(alpha), res) if alpha != 1.0 else res)

    def _cauchy_inversed(self, ast_to_transform):
        return utils.add(
            ast.NumVal(0.5),
            utils.div(
                ast.AtanExpr(ast_to_transform),
                ast.NumVal(math.pi)))

    def _get_power(self):
        raise NotImplementedError

    def _get_alpha(self):
        raise NotImplementedError


class StatsmodelsGLMModelAssembler(GLMMixin, StatsmodelsLinearModelAssembler):

    def _get_link_function_name(self):
        return type(self.model.model.family.link).__name__

    def _get_supported_inversed_funs(self):
        return {
            "logit": self._logit_inversed,
            "power": self._power_inversed,
            "inverse_power": self._inverse_power_inversed,
            "sqrt": self._sqrt_inversed,
            "inverse_squared": self._inverse_squared_inversed,
            "identity": self._identity_inversed,
            "log": self._log_inversed,
            "cloglog": self._cloglog_inversed,
            "negativebinomial": self._negativebinomial_inversed,
            "nbinom": self._negativebinomial_inversed,
            "cauchy": self._cauchy_inversed
        }

    def _get_power(self):
        return self.model.model.family.link.power

    def _get_alpha(self):
        return self.model.model.family.link.alpha


class StatsmodelsModelAssemblerSelector(ModelAssembler):

    def __init__(self, model):
        underlying_model = type(model.model).__name__
        if underlying_model == "GLM":
            self.assembler = StatsmodelsGLMModelAssembler(model)
        elif underlying_model in {"GLS",
                                  "GLSAR",
                                  "OLS",
                                  "WLS"}:
            self.assembler = StatsmodelsLinearModelAssembler(model)
        else:
            raise NotImplementedError(
                f"Model '{underlying_model}' is not supported")

    def assemble(self):
        return self.assembler.assemble()


class SklearnGLMModelAssembler(GLMMixin, SklearnLinearModelAssembler):

    def _get_link_function_name(self):
        return type(self.model._link_instance).__name__

    def _get_supported_inversed_funs(self):
        return {
            "identitylink": self._identity_inversed,
            "loglink": self._log_inversed,
            "logitlink": self._logit_inversed
        }


def _linear_to_ast(coef, intercept):
    feature_weight_mul_ops = [
        utils.mul(ast.FeatureRef(index), ast.NumVal(value))
        for index, value in enumerate(coef)
    ]
    return utils.apply_op_to_expressions(
        ast.BinNumOpType.ADD,
        ast.NumVal(intercept),
        *feature_weight_mul_ops)
