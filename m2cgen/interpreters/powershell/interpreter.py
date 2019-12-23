import os

from m2cgen import ast
from m2cgen.interpreters import utils, mixins
from m2cgen.interpreters.powershell.code_generator \
    import PowershellCodeGenerator
from m2cgen.interpreters.interpreter import ToCodeInterpreter


class PowershellInterpreter(ToCodeInterpreter,
                            mixins.LinearAlgebraMixin):

    supported_bin_vector_ops = {
        ast.BinNumOpType.ADD: "Add-Vectors",
    }

    supported_bin_vector_num_ops = {
        ast.BinNumOpType.MUL: "Mul-Vector-Number",
    }

    exponent_function_name = "[math]::Exp"
    power_function_name = "[math]::Pow"
    tanh_function_name = "[math]::Tanh"

    def __init__(self, indent=4, *args, **kwargs):
        cg = PowershellCodeGenerator(indent=indent)
        kwargs["feature_array_name"] = "InputVector"
        super(PowershellInterpreter, self).__init__(cg, *args, **kwargs)

    def interpret(self, expr):
        self._cg.reset_state()
        self._reset_reused_expr_cache()

        with self._cg.function_definition(
                name="Score",
                args=[(True, self._feature_array_name)],
                is_scalar_output=expr.output_size == 1):
            last_result = self._do_interpret(expr)
            self._cg.add_return_statement(last_result)

        if self.with_linear_algebra:
            filename = os.path.join(
                os.path.dirname(__file__), "linear_algebra.ps1")
            self._cg.prepend_code_lines(utils.get_file_content(filename))

        return self._cg.code

    def interpret_exp_expr(self, expr, **kwargs):
        nested_result = self._do_interpret(expr.expr, **kwargs)
        return self._cg.math_function_invocation(
            self.exponent_function_name, nested_result)

    def interpret_tanh_expr(self, expr, **kwargs):
        nested_result = self._do_interpret(expr.expr, **kwargs)
        return self._cg.math_function_invocation(
            self.tanh_function_name, nested_result)

    def interpret_pow_expr(self, expr, **kwargs):
        base_result = self._do_interpret(expr.base_expr, **kwargs)
        exp_result = self._do_interpret(expr.exp_expr, **kwargs)
        return self._cg.math_function_invocation(
            self.power_function_name, base_result, exp_result)
