from pathlib import Path

from m2cgen.ast import BinNumOpType
from m2cgen.interpreters.interpreter import ImperativeToCodeInterpreter
from m2cgen.interpreters.mixins import BinExpressionDepthTrackingMixin, LinearAlgebraMixin, PowExprFunctionMixin
from m2cgen.interpreters.fortran.code_generator import FortranCodeGenerator
from m2cgen.interpreters.utils import get_file_content


class FortranInterpreter(ImperativeToCodeInterpreter,
                         PowExprFunctionMixin,
                         BinExpressionDepthTrackingMixin,
                         LinearAlgebraMixin):
    # needs to be tested.
    bin_depth_threshold = 55

    supported_bin_vector_ops = {
        BinNumOpType.ADD: "add_vectors",
    }

    supported_bin_vector_num_ops = {
        BinNumOpType.MUL: "mul_vector_number",
    }

    abs_function_name = "ABS"
    atan_function_name = "ATAN"
    exponent_function_name = "EXP"
    logarithm_function_name = "LOG"
    log1p_function_name = "LOG1P"
    sigmoid_function_name = "SIGMOID"
    softmax_function_name = "SOFTMAX"
    sqrt_function_name = "SQRT"
    tanh_function_name = "TANH"

    pow_operator = "**"

    with_sigmoid_expr = False
    with_softmax_expr = False
    with_log1p_expr = False

    def __init__(self, indent=4, function_name="score", *args, **kwargs):
        self.function_name = function_name

        cg = FortranCodeGenerator(indent=indent)
        super().__init__(cg, *args, **kwargs)

    def interpret(self, expr):
        self._cg.reset_state()
        self._reset_reused_expr_cache()

        with self._cg.function_definition(
                name=self.function_name,
                args=[self._feature_array_name],
                output_size=expr.output_size,
        ):
            last_result = self._do_interpret(expr)
            self._cg.add_return_statement(last_result, self.function_name, expr.output_size)

        current_dir = Path(__file__).absolute().parent

        if self.with_linear_algebra \
                or self.with_softmax_expr \
                or self.with_sigmoid_expr \
                or self.with_log1p_expr:
            self._cg.add_code_line("contains")

        if self.with_linear_algebra:
            filename = current_dir / "linear_algebra.f90"
            self._add_contain_statement(filename)

        if self.with_softmax_expr:
            filename = current_dir / "softmax.f90"
            self._add_contain_statement(filename)

        if self.with_sigmoid_expr:
            filename = current_dir / "sigmoid.f90"
            self._add_contain_statement(filename)

        if self.with_log1p_expr:
            filename = current_dir / "log1p.f90"
            self._add_contain_statement(filename)

        return self._cg.finalize_and_get_generated_code()

    def _add_contain_statement(self, filename):
        self._cg.increase_indent()
        self._cg.add_code_lines(get_file_content(filename))
        self._cg.decrease_indent()

    def interpret_abs_expr(self, expr, **kwargs):
        nested_result = self._do_interpret(expr.expr, **kwargs)
        return self._cg.function_invocation(
            self.abs_function_name, nested_result)

    def interpret_log1p_expr(self, expr, **kwargs):
        self.with_log1p_expr = True
        return super().interpret_softmax_expr(expr, **kwargs)

    def interpret_softmax_expr(self, expr, **kwargs):
        self.with_softmax_expr = True
        return super().interpret_softmax_expr(expr, **kwargs)

    def interpret_sigmoid_expr(self, expr, **kwargs):
        self.with_sigmoid_expr = True
        return super().interpret_sigmoid_expr(expr, **kwargs)
