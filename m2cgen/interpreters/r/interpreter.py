from m2cgen.interpreters import mixins
from m2cgen.interpreters.interpreter import ImperativeToCodeInterpreter
from m2cgen.interpreters.r.code_generator import RCodeGenerator


class RInterpreter(ImperativeToCodeInterpreter,
                   mixins.LinearAlgebraMixin,
                   mixins.BinExpressionDepthTrackingMixin,
                   mixins.SubroutinesMixin):

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
    sqrt_function_name = "sqrt"
    tanh_function_name = "tanh"

    def __init__(self, indent=4, function_name="score", *args, **kwargs):
        self.indent = indent
        self.function_name = function_name

        super().__init__(None, *args, **kwargs)

    def interpret(self, expr):
        top_cg = self.create_code_generator()

        self.enqueue_subroutine(self.function_name, expr)
        self.process_subroutine_queue(top_cg)

        return top_cg.finalize_and_get_generated_code()

    def create_code_generator(self):
        return RCodeGenerator(indent=self.indent)

    def interpret_pow_expr(self, expr, **kwargs):
        base_result = self._do_interpret(expr.base_expr, **kwargs)
        exp_result = self._do_interpret(expr.exp_expr, **kwargs)
        return self._cg.infix_expression(
            left=base_result, right=exp_result, op="^")

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
