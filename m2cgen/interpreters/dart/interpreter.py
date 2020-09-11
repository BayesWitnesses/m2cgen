import os

from m2cgen import ast
from m2cgen.interpreters import mixins
from m2cgen.interpreters import utils
from m2cgen.interpreters.interpreter import ImperativeToCodeInterpreter
from m2cgen.interpreters.dart.code_generator import DartCodeGenerator


class DartInterpreter(ImperativeToCodeInterpreter,
                      mixins.LinearAlgebraMixin,
                      mixins.BinExpressionDepthTrackingMixin):

    supported_bin_vector_ops = {
        ast.BinNumOpType.ADD: "addVectors",
    }

    supported_bin_vector_num_ops = {
        ast.BinNumOpType.MUL: "mulVectorNumber",
    }

    bin_depth_threshold = 465

    abs_function_name = "abs"
    atan_function_name = "atan"
    exponent_function_name = "exp"
    logarithm_function_name = "log"
    log1p_function_name = "log1p"
    power_function_name = "pow"
    sqrt_function_name = "sqrt"
    tanh_function_name = "tanh"

    with_log1p_expr = False
    with_tanh_expr = False

    def __init__(self, indent=4, function_name="score", *args, **kwargs):
        self.indent = indent
        self.function_name = function_name

        cg = DartCodeGenerator(indent=indent)
        super().__init__(cg, *args, **kwargs)

    def interpret(self, expr):
        self._cg.reset_state()
        self._reset_reused_expr_cache()

        args = [(True, self._feature_array_name)]

        with self._cg.function_definition(
                name=self.function_name,
                args=args,
                is_vector_output=expr.output_size > 1):
            last_result = self._do_interpret(expr)
            self._cg.add_return_statement(last_result)

        if self.with_linear_algebra:
            filename = os.path.join(
                os.path.dirname(__file__), "linear_algebra.dart")
            self._cg.add_code_lines(utils.get_file_content(filename))

        if self.with_log1p_expr:
            filename = os.path.join(
                os.path.dirname(__file__), "log1p.dart")
            self._cg.add_code_lines(utils.get_file_content(filename))

        if self.with_tanh_expr:
            filename = os.path.join(
                os.path.dirname(__file__), "tanh.dart")
            self._cg.add_code_lines(utils.get_file_content(filename))

        if self.with_math_module:
            self._cg.add_dependency("dart:math")

        return self._cg.finalize_and_get_generated_code()

    def interpret_abs_expr(self, expr, **kwargs):
        return self._cg.method_invocation(
            method_name=self.abs_function_name,
            obj=self._do_interpret(expr.expr, **kwargs),
            args=[])

    def interpret_log1p_expr(self, expr, **kwargs):
        self.with_log1p_expr = True
        return super().interpret_log1p_expr(expr, **kwargs)

    def interpret_tanh_expr(self, expr, **kwargs):
        self.with_tanh_expr = True
        return super().interpret_tanh_expr(expr, **kwargs)
