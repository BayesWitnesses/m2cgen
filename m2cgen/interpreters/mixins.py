import sys

from m2cgen import ast
from m2cgen.interpreters.interpreter import BaseAstToCodeInterpreter


class BinExpressionDepthTrackingMixin(BaseAstToCodeInterpreter):
    """
    This mixin provides an ability to call a custom cook when depth of the
    binary expression reaches certain threshold.

    Subclasses must specify value for `bin_depth_threshold`

    By default it creates a variable and assigns it the result of the incoming
    expression interpretation.

    Subclasses may override this default behaviour.
    """

    # disabled by default
    bin_depth_threshold = sys.maxsize

    def _pre_interpret_hook(self, expr, bin_depth=0, **kwargs):
        if not isinstance(expr, ast.BinExpr):
            return None, kwargs

        # We track depth of the binary expressions and call a hook if it
        # reaches specified threshold .
        if bin_depth == self.bin_depth_threshold:
            return self.bin_depth_threshold_hook(expr, **kwargs), kwargs

        kwargs["bin_depth"] = bin_depth + 1
        return None, kwargs

    # Default implementation. Simply adds new variable.
    def bin_depth_threshold_hook(self, expr, **kwargs):
        var_name = self._cg.add_var_declaration(expr.output_size)
        result = self._do_interpret(expr, **kwargs)
        self._cg.add_var_assignment(var_name, result, expr.output_size)
        return var_name


class LinearAlgebraMixin(BaseAstToCodeInterpreter):
    """
    This mixin provides simple way to interpret linear algebra expression as
    function invocation.

    It also provides flag `with_linear_algebra` which indicates whether
    linear algebra was used during interpretation. It can be used to add
    dependencies.
    """

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
