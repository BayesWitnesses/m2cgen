from m2cgen.interpreters import mixins
from m2cgen.interpreters.interpreter import ToCodeInterpreter
from m2cgen.interpreters.r.code_generator import RCodeGenerator


class RInterpreter(ToCodeInterpreter,
                   mixins.LinearAlgebraMixin,
                   mixins.BinExpressionDepthTrackingMixin,
                   mixins.SubroutinesAsFunctionsMixin):

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

    exponent_function_name = "exp"
    tanh_function_name = "tanh"

    def __init__(self, indent=4, *args, **kwargs):
        self.indent = indent

        super().__init__(None, *args, **kwargs)

    def interpret(self, expr):
        top_cg = self.create_code_generator()

        self.enqueue_subroutine("score", expr)
        self.process_subroutine_queue(top_cg)

        return top_cg.code

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
