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
            return self._final_transform(
                _linear_to_ast(coef[0], intercept[0]))

        exprs = []
        for idx in range(coef.shape[0]):
            exprs.append(self._final_transform(
                _linear_to_ast(coef[idx], intercept[idx])))
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


class StatsmodelsGLMModelAssembler(StatsmodelsLinearModelAssembler):

    def _final_transform(self, ast_to_transform):
        link_function = type(self.model.model.family.link).__name__
        link_function_lower = link_function.lower()
        supported_functions = {
            "logit": self._logit,
            "power": self._power,
            "inverse_power": self._inverse_power,
            "sqrt": self._sqrt,
            "inverse_squared": self._inverse_squared,
            "identity": self._identity,
            "log": self._log,
            "cloglog": self._cloglog,
            "negativebinomial": self._negativebinomial,
            "nbinom": self._negativebinomial
        }
        if link_function_lower not in supported_functions:
            raise ValueError(
                "Unsupported link function '{}'".format(link_function))
        link_fun = supported_functions[link_function_lower]
        return link_fun(ast_to_transform)

    def _logit(self, ast_to_transform):
        return utils.div(
            ast.NumVal(1.0),
            utils.add(
                ast.NumVal(1.0),
                ast.ExpExpr(
                    utils.sub(
                        ast.NumVal(0.0),
                        ast_to_transform))))

    def _power(self, ast_to_transform):
        power = self.model.model.family.link.power
        if power == 1:
            return self._identity(ast_to_transform)
        elif power == -1:
            return self._inverse_power(ast_to_transform)
        elif power == 2:
            return ast.SqrtExpr(ast_to_transform)
        elif power == -2:
            return self._inverse_squared(ast_to_transform)
        elif power < 0:  # some languages may not support negative exponent
            return utils.div(
                ast.NumVal(1.0),
                ast.PowExpr(ast_to_transform, ast.NumVal(1 / -power)))
        else:
            return ast.PowExpr(ast_to_transform, ast.NumVal(1 / power))

    def _inverse_power(self, ast_to_transform):
        return utils.div(ast.NumVal(1.0), ast_to_transform)

    def _sqrt(self, ast_to_transform):
        return ast.PowExpr(ast_to_transform, ast.NumVal(2))

    def _inverse_squared(self, ast_to_transform):
        return utils.div(ast.NumVal(1.0), ast.SqrtExpr(ast_to_transform))

    def _identity(self, ast_to_transform):
        return ast_to_transform

    def _log(self, ast_to_transform):
        return ast.ExpExpr(ast_to_transform)

    def _cloglog(self, ast_to_transform):
        return utils.sub(
            ast.NumVal(1.0),
            ast.ExpExpr(
                utils.sub(
                    ast.NumVal(0.0),
                    ast.ExpExpr(ast_to_transform))))

    def _negativebinomial(self, ast_to_transform):
        return utils.div(
            ast.NumVal(-1.0),
            utils.mul(
                ast.NumVal(self.model.model.family.link.alpha),
                utils.sub(
                    ast.NumVal(1.0),
                    ast.ExpExpr(
                        utils.sub(
                            ast.NumVal(0.0),
                            ast_to_transform)))))


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
                "Model '{}' is not supported".format(underlying_model))

    def assemble(self):
        return self.assembler.assemble()


def _linear_to_ast(coef, intercept):
    feature_weight_mul_ops = []

    for index, value in enumerate(coef):
        feature_weight_mul_ops.append(
            utils.mul(ast.FeatureRef(index), ast.NumVal(value)))

    return utils.apply_op_to_expressions(
        ast.BinNumOpType.ADD,
        ast.NumVal(intercept),
        *feature_weight_mul_ops)
