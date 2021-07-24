from pathlib import Path

from m2cgen.ast import BinNumOpType
from m2cgen.interpreters.interpreter import ImperativeToCodeInterpreter
from m2cgen.interpreters.mixins import LinearAlgebraMixin
from m2cgen.interpreters.powershell.code_generator import PowershellCodeGenerator
from m2cgen.interpreters.utils import get_file_content


class PowershellInterpreter(ImperativeToCodeInterpreter,
                            LinearAlgebraMixin):

    supported_bin_vector_ops = {
        BinNumOpType.ADD: "Add-Vectors",
    }

    supported_bin_vector_num_ops = {
        BinNumOpType.MUL: "Mul-Vector-Number",
    }

    abs_function_name = "[math]::Abs"
    atan_function_name = "[math]::Atan"
    exponent_function_name = "[math]::Exp"
    logarithm_function_name = "[math]::Log"
    log1p_function_name = "Log1p"
    power_function_name = "[math]::Pow"
    sigmoid_function_name = "Sigmoid"
    softmax_function_name = "Softmax"
    sqrt_function_name = "[math]::Sqrt"
    tanh_function_name = "[math]::Tanh"

    with_log1p_expr = False
    with_sigmoid_expr = False
    with_softmax_expr = False

    def __init__(self, indent=4, function_name="Score", *args, **kwargs):
        self.function_name = function_name

        cg = PowershellCodeGenerator(indent=indent)
        kwargs["feature_array_name"] = "InputVector"
        super().__init__(cg, *args, **kwargs)

    def interpret(self, expr):
        self._cg.reset_state()
        self._reset_reused_expr_cache()

        with self._cg.function_definition(
                name=self.function_name,
                args=[(True, self._feature_array_name)]):
            last_result = self._do_interpret(expr)
            self._cg.add_return_statement(last_result)

        current_dir = Path(__file__).absolute().parent

        if self.with_linear_algebra:
            filename = current_dir / "linear_algebra.ps1"
            self._cg.add_code_lines(get_file_content(filename))

        if self.with_log1p_expr:
            filename = current_dir / "log1p.ps1"
            self._cg.add_code_lines(get_file_content(filename))

        if self.with_softmax_expr:
            filename = current_dir / "softmax.ps1"
            self._cg.add_code_lines(get_file_content(filename))

        if self.with_sigmoid_expr:
            filename = current_dir / "sigmoid.ps1"
            self._cg.add_code_lines(get_file_content(filename))

        return self._cg.finalize_and_get_generated_code()

    def interpret_abs_expr(self, expr, **kwargs):
        nested_result = self._do_interpret(expr.expr, **kwargs)
        return self._cg.math_function_invocation(
            self.abs_function_name, nested_result)

    def interpret_atan_expr(self, expr, **kwargs):
        nested_result = self._do_interpret(expr.expr, **kwargs)
        return self._cg.math_function_invocation(
            self.atan_function_name, nested_result)

    def interpret_exp_expr(self, expr, **kwargs):
        nested_result = self._do_interpret(expr.expr, **kwargs)
        return self._cg.math_function_invocation(
            self.exponent_function_name, nested_result)

    def interpret_log_expr(self, expr, **kwargs):
        nested_result = self._do_interpret(expr.expr, **kwargs)
        return self._cg.math_function_invocation(
            self.logarithm_function_name, nested_result)

    def interpret_log1p_expr(self, expr, **kwargs):
        self.with_log1p_expr = True
        return super().interpret_log1p_expr(expr, **kwargs)

    def interpret_sqrt_expr(self, expr, **kwargs):
        nested_result = self._do_interpret(expr.expr, **kwargs)
        return self._cg.math_function_invocation(
            self.sqrt_function_name, nested_result)

    def interpret_tanh_expr(self, expr, **kwargs):
        nested_result = self._do_interpret(expr.expr, **kwargs)
        return self._cg.math_function_invocation(
            self.tanh_function_name, nested_result)

    def interpret_pow_expr(self, expr, **kwargs):
        base_result = self._do_interpret(expr.base_expr, **kwargs)
        exp_result = self._do_interpret(expr.exp_expr, **kwargs)
        return self._cg.math_function_invocation(
            self.power_function_name, base_result, exp_result)

    def interpret_softmax_expr(self, expr, **kwargs):
        self.with_softmax_expr = True
        return super().interpret_softmax_expr(expr, **kwargs)

    def interpret_sigmoid_expr(self, expr, **kwargs):
        self.with_sigmoid_expr = True
        return super().interpret_sigmoid_expr(expr, **kwargs)
