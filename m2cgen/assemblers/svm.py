import numpy as np

from m2cgen import ast
from m2cgen.assemblers import utils
from m2cgen.assemblers.base import ModelAssembler


class BaseSVMModelAssembler(ModelAssembler):

    def __init__(self, model):
        super().__init__(model)

        kernel_type = model.kernel
        supported_kernels = self._get_supported_kernels()
        if kernel_type not in supported_kernels:
            raise ValueError(f"Unsupported kernel type '{kernel_type}'")
        self._kernel_fun = supported_kernels[kernel_type]

        gamma = self._get_gamma()
        self._gamma_expr = ast.NumVal(gamma)
        self._neg_gamma_expr = ast.NumVal(-gamma)

        self._output_size = self._get_output_size()

    def assemble(self):
        if self._output_size > 1:
            return self._assemble_multi_class_output()
        else:
            return self._assemble_single_output()

    def _assemble_single_output(self, idx=0):
        support_vectors = self.model.support_vectors_
        coef = self._get_single_coef(idx)
        intercept = self._get_single_intercept(idx)

        kernel_exprs = self._apply_kernel(support_vectors)

        kernel_weight_mul_ops = [
            utils.mul(kernel_exprs[index], ast.NumVal(value))
            for index, value in enumerate(coef)
        ]

        return utils.apply_op_to_expressions(
            ast.BinNumOpType.ADD,
            ast.NumVal(intercept),
            *kernel_weight_mul_ops)

    def _apply_kernel(self, support_vectors, to_reuse=False):
        kernel_exprs = []
        for v in support_vectors:
            kernel = self._kernel_fun(v)
            kernel.to_reuse = to_reuse
            kernel_exprs.append(kernel)
        return kernel_exprs

    def _get_supported_kernels(self):
        return {
            "rbf": self._rbf_kernel,
            "sigmoid": self._sigmoid_kernel,
            "poly": self._poly_kernel,
            "linear": self._linear_kernel
        }

    def _get_gamma(self):
        raise NotImplementedError

    def _get_output_size(self):
        raise NotImplementedError

    def _assemble_multi_class_output(self):
        raise NotImplementedError

    def _get_single_coef(self, idx=0):
        raise NotImplementedError

    def _get_single_intercept(self, idx=0):
        raise NotImplementedError


class SklearnSVMModelAssembler(BaseSVMModelAssembler):

    def _get_gamma(self):
        return self.model._gamma

    def _get_output_size(self):
        output_size = 1
        if type(self.model).__name__ in {"SVC", "NuSVC"}:
            n_classes = len(self.model.n_support_)
            if n_classes > 2:
                output_size = n_classes
        return output_size

    def _assemble_multi_class_output(self):
        support_vectors = self.model.support_vectors_
        coef = self.model.dual_coef_
        intercept = self.model.intercept_

        n_support = self.model.n_support_
        n_support_len = len(n_support)

        kernel_exprs = self._apply_kernel(support_vectors, to_reuse=True)

        support_ranges = []
        for i in range(n_support_len):
            range_start = sum(n_support[:i])
            range_end = range_start + n_support[i]
            support_ranges.append((range_start, range_end))

        # One-vs-one decisions.
        decisions = []
        for i in range(n_support_len):
            for j in range(i + 1, n_support_len):
                kernel_weight_mul_ops = [
                    utils.mul(kernel_exprs[k], ast.NumVal(coef[i][k]))
                    for k in range(*support_ranges[j])
                ]
                kernel_weight_mul_ops.extend([
                    utils.mul(kernel_exprs[k], ast.NumVal(coef[j - 1][k]))
                    for k in range(*support_ranges[i])
                ])
                decision = utils.apply_op_to_expressions(
                    ast.BinNumOpType.ADD,
                    ast.NumVal(intercept[len(decisions)]),
                    *kernel_weight_mul_ops
                )
                decisions.append(decision)

        return ast.VectorVal(decisions)

    def _get_single_coef(self, idx=0):
        return self.model.dual_coef_[idx]

    def _get_single_intercept(self, idx=0):
        return self.model.intercept_[idx]

    def _rbf_kernel(self, support_vector):
        elem_wise = [
            ast.PowExpr(
                utils.sub(ast.NumVal(support_element), ast.FeatureRef(i)),
                ast.NumVal(2.0)
            )
            for i, support_element in enumerate(support_vector)
        ]
        kernel = utils.apply_op_to_expressions(ast.BinNumOpType.ADD,
                                               *elem_wise)
        kernel = utils.mul(self._neg_gamma_expr, kernel)
        return ast.ExpExpr(kernel)

    def _sigmoid_kernel(self, support_vector):
        kernel = self._linear_kernel_with_gamma_and_coef(support_vector)
        return ast.TanhExpr(kernel)

    def _poly_kernel(self, support_vector):
        kernel = self._linear_kernel_with_gamma_and_coef(support_vector)
        return ast.PowExpr(kernel, ast.NumVal(self.model.degree))

    def _linear_kernel(self, support_vector):
        elem_wise = [
            utils.mul(ast.NumVal(support_element), ast.FeatureRef(i))
            for i, support_element in enumerate(support_vector)
        ]
        return utils.apply_op_to_expressions(ast.BinNumOpType.ADD, *elem_wise)

    def _linear_kernel_with_gamma_and_coef(self, support_vector):
        kernel = self._linear_kernel(support_vector)
        kernel = utils.mul(self._gamma_expr, kernel)
        return utils.add(kernel, ast.NumVal(self.model.coef0))


class LightningSVMModelAssembler(SklearnSVMModelAssembler):

    def _get_supported_kernels(self):
        kernels = super()._get_supported_kernels()
        kernels["cosine"] = self._cosine_kernel
        return kernels

    def _get_gamma(self):
        return self.model.gamma

    def _get_output_size(self):
        output_size = 1
        n_classes = len(self.model.classes_)
        if n_classes > 2:
            output_size = n_classes
        return output_size

    def _assemble_multi_class_output(self):
        exprs = [
            self._assemble_single_output(idx)
            for idx in range(self.model.classes_.shape[0])
        ]
        return ast.VectorVal(exprs)

    def _get_single_coef(self, idx=0):
        return self.model.coef_[idx]

    def _get_single_intercept(self, idx=0):
        return 0.0

    def _cosine_kernel(self, support_vector):
        support_vector_norm = np.linalg.norm(support_vector)
        if support_vector_norm == 0.0:
            support_vector_norm = 1.0
        feature_norm = ast.SqrtExpr(
            utils.apply_op_to_expressions(
                ast.BinNumOpType.ADD,
                *[utils.mul(ast.FeatureRef(i), ast.FeatureRef(i))
                  for i in range(len(support_vector))]),
            to_reuse=True)
        safe_feature_norm = ast.IfExpr(
            utils.eq(feature_norm, ast.NumVal(0.0)),
            ast.NumVal(1.0),
            feature_norm)
        kernel = self._linear_kernel(support_vector / support_vector_norm)
        kernel = utils.div(kernel, safe_feature_norm)
        return kernel
