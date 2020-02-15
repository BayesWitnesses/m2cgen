import os

from m2cgen import ast
from m2cgen.interpreters import mixins
from m2cgen.interpreters import utils
from m2cgen.interpreters.interpreter import ToCodeInterpreter
from m2cgen.interpreters.dart.code_generator import DartCodeGenerator


class DartInterpreter(ToCodeInterpreter, mixins.LinearAlgebraMixin):

    supported_bin_vector_ops = {
        ast.BinNumOpType.ADD: "addVectors",
    }

    supported_bin_vector_num_ops = {
        ast.BinNumOpType.MUL: "mulVectorNumber",
    }

    exponent_function_name = "exp"
    power_function_name = "pow"
    tanh_function_name = "tanh"

    with_tanh_expr = False

    def __init__(self, class_name="Model", indent=4,
                 *args, **kwargs):
        self.class_name = class_name
        self.indent = indent

        cg = DartCodeGenerator(indent=indent)
        super(DartInterpreter, self).__init__(cg, *args, **kwargs)

    def interpret(self, expr):
        self._cg.reset_state()
        self._reset_reused_expr_cache()

        method_name = "score"
        args = [(True, self._feature_array_name)]

        with self._cg.class_definition(self.class_name):
            with self._cg.method_definition(
                    name=method_name,
                    args=args,
                    is_vector_output=expr.output_size > 1,
                    is_private=False):
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
