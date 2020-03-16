import os

from m2cgen import ast
from m2cgen.interpreters import mixins
from m2cgen.interpreters import utils
from m2cgen.interpreters.interpreter import ToCodeInterpreter
from m2cgen.interpreters.dart.code_generator import DartCodeGenerator


class DartInterpreter(ToCodeInterpreter,
                      mixins.LinearAlgebraMixin,
                      mixins.BinExpressionDepthTrackingMixin):

    supported_bin_vector_ops = {
        ast.BinNumOpType.ADD: "addVectors",
    }

    supported_bin_vector_num_ops = {
        ast.BinNumOpType.MUL: "mulVectorNumber",
    }

    bin_depth_threshold = 465

    exponent_function_name = "exp"
    power_function_name = "pow"
    sqrt_function_name = "sqrt"
    tanh_function_name = "tanh"

    with_tanh_expr = False

    def __init__(self, indent=4, function_name="score", *args, **kwargs):
        self.indent = indent
        self.function_name = function_name

        cg = DartCodeGenerator(indent=indent)
        super(DartInterpreter, self).__init__(cg, *args, **kwargs)

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

        # Use own tanh function in order to be compatible with Dart
        if self.with_tanh_expr:
            filename = os.path.join(
                os.path.dirname(__file__), "tanh.dart")
            self._cg.add_code_lines(utils.get_file_content(filename))

        if self.with_math_module:
            self._cg.add_dependency("dart:math")

        return self._cg.code

    def interpret_tanh_expr(self, expr, **kwargs):
        self.with_tanh_expr = True
        return super(
            DartInterpreter, self).interpret_tanh_expr(expr, **kwargs)
