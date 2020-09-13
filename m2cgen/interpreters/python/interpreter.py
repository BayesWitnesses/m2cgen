import os

from m2cgen import ast
from m2cgen.interpreters import mixins, utils
from m2cgen.interpreters.interpreter import ImperativeToCodeInterpreter
from m2cgen.interpreters.python.code_generator import PythonCodeGenerator


class PythonInterpreter(ImperativeToCodeInterpreter,
                        mixins.BinExpressionDepthTrackingMixin,
                        mixins.LinearAlgebraMixin):

    # 60 raises MemoryError for some SVM models with RBF kernel.
    bin_depth_threshold = 55

    supported_bin_vector_ops = {
        ast.BinNumOpType.ADD: "add_vectors",
    }

    supported_bin_vector_num_ops = {
        ast.BinNumOpType.MUL: "mul_vector_number",
    }

    abs_function_name = "abs"
    atan_function_name = "math.atan"
    exponent_function_name = "math.exp"
    logarithm_function_name = "math.log"
    log1p_function_name = "math.log1p"
    power_function_name = "math.pow"
    sqrt_function_name = "math.sqrt"
    tanh_function_name = "math.tanh"

    def __init__(self, indent=4, function_name="score", *args, **kwargs):
        self.function_name = function_name

        cg = PythonCodeGenerator(indent=indent)
        super().__init__(cg, *args, **kwargs)

    def interpret(self, expr):
        self._cg.reset_state()
        self._reset_reused_expr_cache()

        with self._cg.function_definition(
                name=self.function_name,
                args=[self._feature_array_name]):
            last_result = self._do_interpret(expr)
            self._cg.add_return_statement(last_result)

        if self.with_linear_algebra:
            filename = os.path.join(
                os.path.dirname(__file__), "linear_algebra.py")
            self._cg.prepend_code_lines(utils.get_file_content(filename))

        if self.with_math_module:
            self._cg.add_dependency("math")

        return self._cg.finalize_and_get_generated_code()

    def interpret_abs_expr(self, expr, **kwargs):
        nested_result = self._do_interpret(expr.expr, **kwargs)
        return self._cg.function_invocation(
            self.abs_function_name, nested_result)
