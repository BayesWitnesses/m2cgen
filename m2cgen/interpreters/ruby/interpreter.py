from pathlib import Path

from m2cgen.ast import BinNumOpType
from m2cgen.interpreters.interpreter import ImperativeToCodeInterpreter
from m2cgen.interpreters.mixins import LinearAlgebraMixin, PowExprInfixMixin
from m2cgen.interpreters.ruby.code_generator import RubyCodeGenerator
from m2cgen.interpreters.utils import get_file_content


class RubyInterpreter(ImperativeToCodeInterpreter,
                      PowExprInfixMixin,
                      LinearAlgebraMixin):

    supported_bin_vector_ops = {
        BinNumOpType.ADD: "add_vectors",
    }

    supported_bin_vector_num_ops = {
        BinNumOpType.MUL: "mul_vector_number",
    }

    abs_function_name = "abs"
    atan_function_name = "Math.atan"
    exponent_function_name = "Math.exp"
    logarithm_function_name = "Math.log"
    log1p_function_name = "log1p"
    sigmoid_function_name = "sigmoid"
    softmax_function_name = "softmax"
    sqrt_function_name = "Math.sqrt"
    tanh_function_name = "Math.tanh"

    with_log1p_expr = False
    with_sigmoid_expr = False
    with_softmax_expr = False

    def __init__(self, indent=4, function_name="score", *args, **kwargs):
        self.function_name = function_name

        cg = RubyCodeGenerator(indent=indent)
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
            filename = current_dir / "linear_algebra.rb"
            self._cg.add_code_lines(get_file_content(filename))

        if self.with_log1p_expr:
            filename = current_dir / "log1p.rb"
            self._cg.add_code_lines(get_file_content(filename))

        if self.with_softmax_expr:
            filename = current_dir / "softmax.rb"
            self._cg.add_code_lines(get_file_content(filename))

        if self.with_sigmoid_expr:
            filename = current_dir / "sigmoid.rb"
            self._cg.add_code_lines(get_file_content(filename))

        return self._cg.finalize_and_get_generated_code()

    def interpret_bin_num_expr(self, expr, **kwargs):
        if expr.op == BinNumOpType.DIV:
            # Always force float result
            return self._cg.method_invocation(
                method_name="fdiv",
                obj=self._do_interpret(expr.left, **kwargs),
                args=[self._do_interpret(expr.right, **kwargs)])
        else:
            return super().interpret_bin_num_expr(expr, **kwargs)

    def interpret_abs_expr(self, expr, **kwargs):
        return self._cg.method_invocation(
            method_name=self.abs_function_name,
            obj=self._do_interpret(expr.expr, **kwargs),
            args=[])

    def interpret_log1p_expr(self, expr, **kwargs):
        self.with_log1p_expr = True
        return super().interpret_log1p_expr(expr, **kwargs)

    def interpret_softmax_expr(self, expr, **kwargs):
        self.with_softmax_expr = True
        return super().interpret_softmax_expr(expr, **kwargs)

    def interpret_sigmoid_expr(self, expr, **kwargs):
        self.with_sigmoid_expr = True
        return super().interpret_sigmoid_expr(expr, **kwargs)
