from pathlib import Path

from m2cgen.ast import BinNumOpType
from m2cgen.interpreters.interpreter import ImperativeToCodeInterpreter
from m2cgen.interpreters.mixins import BinExpressionDepthTrackingMixin, LinearAlgebraMixin, PowExprFunctionMixin
from m2cgen.interpreters.python.code_generator import PythonCodeGenerator
from m2cgen.interpreters.utils import get_file_content


class PythonInterpreter(ImperativeToCodeInterpreter,
                        PowExprFunctionMixin,
                        BinExpressionDepthTrackingMixin,
                        LinearAlgebraMixin):

    # 60 raises MemoryError for some SVM models with RBF kernel.
    bin_depth_threshold = 55

    supported_bin_vector_ops = {
        BinNumOpType.ADD: "add_vectors",
    }

    supported_bin_vector_num_ops = {
        BinNumOpType.MUL: "mul_vector_number",
    }

    abs_function_name = "abs"
    atan_function_name = "math.atan"
    exponent_function_name = "math.exp"
    logarithm_function_name = "math.log"
    log1p_function_name = "math.log1p"
    power_function_name = "math.pow"
    sigmoid_function_name = "sigmoid"
    softmax_function_name = "softmax"
    sqrt_function_name = "math.sqrt"
    tanh_function_name = "math.tanh"

    with_sigmoid_expr = False
    with_softmax_expr = False

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

        current_dir = Path(__file__).absolute().parent

        if self.with_linear_algebra:
            filename = current_dir / "linear_algebra.py"
            self._cg.prepend_code_lines(get_file_content(filename))

        if self.with_softmax_expr:
            filename = current_dir / "softmax.py"
            self._cg.prepend_code_lines(get_file_content(filename))

        if self.with_sigmoid_expr:
            filename = current_dir / "sigmoid.py"
            self._cg.prepend_code_lines(get_file_content(filename))

        if self.with_math_module:
            self._cg.add_dependency("math")

        return self._cg.finalize_and_get_generated_code()

    def interpret_abs_expr(self, expr, **kwargs):
        nested_result = self._do_interpret(expr.expr, **kwargs)
        return self._cg.function_invocation(
            self.abs_function_name, nested_result)

    def interpret_softmax_expr(self, expr, **kwargs):
        self.with_softmax_expr = True
        return super().interpret_softmax_expr(expr, **kwargs)

    def interpret_sigmoid_expr(self, expr, **kwargs):
        self.with_sigmoid_expr = True
        return super().interpret_sigmoid_expr(expr, **kwargs)
