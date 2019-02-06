import sys

from m2cgen import ast
from m2cgen.interpreters.interpreter import BaseAstToCodeInterpreter


class BinExpressionDepthTrackingMixin(BaseAstToCodeInterpreter):

    # disabled by default
    bin_depth_threshold = sys.maxsize

    def _pre_interpret_hook(self, expr, bin_depth=None, **kwargs):
        if not isinstance(expr, ast.BinExpr):
            return expr, kwargs

        # We track depth of the binary expressions and call a hook if it
        # exceeds specified limit.
        bin_depth = bin_depth + 1 if bin_depth is not None else 1

        if bin_depth > self.bin_depth_threshold:
            return self.bin_depth_threshold_hook(expr, **kwargs), kwargs

        kwargs["bin_depth"] = bin_depth
        return expr, kwargs

    # Default implementation. Simply adds new variable.
    def bin_depth_threshold_hook(self, expr, **kwargs):
        var_name = self._cg.add_var_declaration(expr.output_size)
        result = self._do_interpret(expr, **kwargs)
        self._cg.add_var_assignment(var_name, result, expr.output_size)
        return var_name


class LinearAlgebraMixin(BaseAstToCodeInterpreter):

    with_linear_algebra = False

    supported_bin_vector_ops = {}
    supported_bin_vector_num_ops = {}

    def interpret_bin_vector_expr(self, expr, extra_func_args=(), **kwargs):
        if expr.op not in self.supported_bin_vector_ops:
            raise NotImplementedError(
                "Op {} is unsupported".format(expr.op.name))

        self.with_linear_algebra = True

        function_name = self.supported_bin_vector_ops[expr.op]

        return self._cg.function_invocation(
            function_name,
            self._do_interpret(expr.left, **kwargs),
            self._do_interpret(expr.right, **kwargs),
            *extra_func_args)

    def interpret_bin_vector_num_expr(self, expr, extra_func_args=(),
                                      **kwargs):
        if expr.op not in self.supported_bin_vector_num_ops:
            raise NotImplementedError(
                "Op {} is unsupported".format(expr.op.name))

        self.with_linear_algebra = True

        function_name = self.supported_bin_vector_num_ops[expr.op]

        return self._cg.function_invocation(
            function_name,
            self._do_interpret(expr.left, **kwargs),
            self._do_interpret(expr.right, **kwargs),
            *extra_func_args)
