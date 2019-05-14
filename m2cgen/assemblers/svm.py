from m2cgen import ast
from m2cgen.assemblers import utils
from m2cgen.assemblers.base import ModelAssembler


class SVMModelAssembler(ModelAssembler):

    def __init__(self, model):
        super().__init__(model)

        supported_kernels = {
            "rbf": self._rbf_kernel,
            "sigmoid": self._sigmoid_kernel,
            "poly": self._poly_kernel,
            "linear": self._linear_kernel
        }
        kernel_type = model.kernel
        if kernel_type not in supported_kernels:
            raise ValueError("Unsupported kernel type {}".format(kernel_type))
        self._kernel_fun = supported_kernels[kernel_type]

        n_features = len(model.support_vectors_[0])

        gamma = model.gamma
        if gamma == "auto" or gamma == "auto_deprecated":
            gamma = 1.0 / n_features
        self._gamma_expr = ast.NumVal(gamma)
        self._neg_gamma_expr = utils.sub(ast.NumVal(0), ast.NumVal(gamma),
                                         to_reuse=True)

        self._output_size = 1
        if type(model).__name__ in ("SVC", "NuSVC"):
            n_classes = len(model.n_support_)
            if n_classes > 2:
                self._output_size = n_classes

    def assemble(self):
        if self._output_size > 1:
            return self._assemble_multi_class_output()
        else:
            return self._assemble_single_output()

    def _assemble_single_output(self):
        support_vectors = self.model.support_vectors_
        coef = self.model.dual_coef_[0]
        intercept = self.model.intercept_[0]

        kernel_exprs = self._apply_kernel(support_vectors)

        kernel_weight_mul_ops = []
        for index, value in enumerate(coef):
            kernel_weight_mul_ops.append(
                utils.mul(kernel_exprs[index], ast.NumVal(value)))

        return utils.apply_op_to_expressions(
            ast.BinNumOpType.ADD,
            ast.NumVal(intercept),
            *kernel_weight_mul_ops)

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

        # TODO convert One-vs-one decisions to One-vs-rest

        return ast.VectorVal(decisions)

    def _apply_kernel(self, support_vectors, to_reuse=False):
        kernel_exprs = []
        for v in support_vectors:
            kernel = self._kernel_fun(v)
            kernel_exprs.append(ast.SubroutineExpr(kernel, to_reuse=to_reuse))
        return kernel_exprs

    def _rbf_kernel(self, support_vector):
        elem_wise = [
            ast.PowExpr(
                utils.sub(ast.NumVal(support_element), ast.FeatureRef(i)),
                ast.NumVal(2)
            )
            for i, support_element in enumerate(support_vector)
        ]
        kernel = utils.apply_op_to_expressions(ast.BinNumOpType.ADD,
                                               *elem_wise)
        kernel = utils.mul(self._neg_gamma_expr, kernel)
        return ast.ExpExpr(kernel)

    def _sigmoid_kernel(self, support_vector):
        kernel = self._linear_kernel_with_gama_and_coef(support_vector)
        return ast.TanhExpr(kernel)

    def _poly_kernel(self, support_vector):
        kernel = self._linear_kernel_with_gama_and_coef(support_vector)
        return ast.PowExpr(kernel, ast.NumVal(self.model.degree))

    def _linear_kernel(self, support_vector):
        elem_wise = [
            utils.mul(ast.NumVal(support_element), ast.FeatureRef(i))
            for i, support_element in enumerate(support_vector)
        ]
        return utils.apply_op_to_expressions(ast.BinNumOpType.ADD, *elem_wise)

    def _linear_kernel_with_gama_and_coef(self, support_vector):
        kernel = self._linear_kernel(support_vector)
        kernel = utils.mul(self._gamma_expr, kernel)
        return utils.add(kernel, ast.NumVal(self.model.coef0))
