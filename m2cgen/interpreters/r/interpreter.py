from pathlib import Path

from m2cgen.interpreters.interpreter import ImperativeToCodeInterpreter
from m2cgen.interpreters.mixins import (
    BinExpressionDepthTrackingMixin,
    LinearAlgebraMixin,
    PowExprInfixMixin,
    SubroutinesMixin
)
from m2cgen.interpreters.r.code_generator import RCodeGenerator
from m2cgen.interpreters.utils import get_file_content


class RInterpreter(ImperativeToCodeInterpreter,
                   PowExprInfixMixin,
                   LinearAlgebraMixin,
                   BinExpressionDepthTrackingMixin,
                   SubroutinesMixin):

    # R doesn't allow to have more than 50 nested if, [, [[, {, ( calls.
    # It raises contextstack overflow error not only for explicitly nested
    # calls, but also if met above mentioned number of parentheses
    # in one expression. Given that there is no way to control
    # the number of parentheses in one expression for now,
    # the following variable set to 50 / 2 value is expected to prevent
    # contextstack overflow error occurrence.
    # This value is just a heuristic and is subject to change in the future
    # based on the users' feedback.
    bin_depth_threshold = 25

    ast_size_check_frequency = 2
    ast_size_per_subroutine_threshold = 200

    abs_function_name = "abs"
    atan_function_name = "atan"
    exponent_function_name = "exp"
    logarithm_function_name = "log"
    log1p_function_name = "log1p"
    sigmoid_function_name = "sigmoid"
    softmax_function_name = "softmax"
    sqrt_function_name = "sqrt"
    tanh_function_name = "tanh"

    pow_operator = "^"

    with_sigmoid_expr = False
    with_softmax_expr = False

    def __init__(self, indent=4, function_name="score", *args, **kwargs):
        self.indent = indent
        self.function_name = function_name

        super().__init__(None, *args, **kwargs)

    def interpret(self, expr):
        top_cg = self.create_code_generator()

        self.enqueue_subroutine(self.function_name, 0, expr)
        self.process_subroutine_queue(top_cg)

        current_dir = Path(__file__).absolute().parent

        if self.with_softmax_expr:
            filename = current_dir / "softmax.r"
            top_cg.prepend_code_lines(get_file_content(filename))

        if self.with_sigmoid_expr:
            filename = current_dir / "sigmoid.r"
            top_cg.prepend_code_lines(get_file_content(filename))

        return top_cg.finalize_and_get_generated_code()

    def create_code_generator(self):
        return RCodeGenerator(indent=self.indent)

    def interpret_softmax_expr(self, expr, **kwargs):
        self.with_softmax_expr = True
        return super().interpret_softmax_expr(expr, **kwargs)

    def interpret_sigmoid_expr(self, expr, **kwargs):
        self.with_sigmoid_expr = True
        return super().interpret_sigmoid_expr(expr, **kwargs)

    def interpret_bin_vector_expr(self, expr, **kwargs):
        self.with_linear_algebra = True
        return self._cg.infix_expression(
            left=self._do_interpret(expr.left, **kwargs),
            op=expr.op.value,
            right=self._do_interpret(expr.right, **kwargs))

    def interpret_bin_vector_num_expr(self, expr, **kwargs):
        self.with_linear_algebra = True
        return self._cg.infix_expression(
            left=self._do_interpret(expr.left, **kwargs),
            op=expr.op.value,
            right=self._do_interpret(expr.right, **kwargs))
