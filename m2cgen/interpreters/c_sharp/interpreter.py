import os

from m2cgen import ast
from m2cgen.interpreters import mixins
from m2cgen.interpreters import utils
from m2cgen.interpreters.interpreter import ImperativeToCodeInterpreter
from m2cgen.interpreters.c_sharp.code_generator import CSharpCodeGenerator


class CSharpInterpreter(ImperativeToCodeInterpreter,
                        mixins.LinearAlgebraMixin):

    supported_bin_vector_ops = {
        ast.BinNumOpType.ADD: "AddVectors",
    }

    supported_bin_vector_num_ops = {
        ast.BinNumOpType.MUL: "MulVectorNumber",
    }

    abs_function_name = "Abs"
    atan_function_name = "Atan"
    exponent_function_name = "Exp"
    logarithm_function_name = "Log"
    log1p_function_name = "Log1p"
    power_function_name = "Pow"
    sqrt_function_name = "Sqrt"
    tanh_function_name = "Tanh"

    with_log1p_expr = False

    def __init__(self, namespace="ML", class_name="Model", indent=4,
                 function_name="Score", *args, **kwargs):
        self.namespace = namespace
        self.class_name = class_name
        self.indent = indent
        self.function_name = function_name

        cg = CSharpCodeGenerator(indent=indent)
        super().__init__(cg, *args, **kwargs)

    def interpret(self, expr):
        self._cg.reset_state()
        self._reset_reused_expr_cache()

        method_name = self.function_name
        args = [(True, self._feature_array_name)]

        with self._cg.namespace_definition(self.namespace):
            with self._cg.class_definition(self.class_name):
                with self._cg.method_definition(
                        name=method_name,
                        args=args,
                        is_vector_output=expr.output_size > 1,
                        modifier="public"):
                    last_result = self._do_interpret(expr)
                    self._cg.add_return_statement(last_result)

                if self.with_linear_algebra:
                    filename = os.path.join(
                        os.path.dirname(__file__), "linear_algebra.cs")
                    self._cg.add_code_lines(utils.get_file_content(filename))

                if self.with_log1p_expr:
                    filename = os.path.join(
                        os.path.dirname(__file__), "log1p.cs")
                    self._cg.add_code_lines(utils.get_file_content(filename))

        if self.with_math_module:
            self._cg.add_dependency("System.Math")

        return self._cg.finalize_and_get_generated_code()

    def interpret_log1p_expr(self, expr, **kwargs):
        self.with_log1p_expr = True
        return super().interpret_log1p_expr(expr, **kwargs)
