import os

from m2cgen import ast
from m2cgen.interpreters import mixins, utils
from m2cgen.interpreters.interpreter import ToCodeInterpreter
from m2cgen.interpreters.r.code_generator import RCodeGenerator


class RInterpreter(ToCodeInterpreter,
                   mixins.LinearAlgebraMixin,
                   mixins.BinExpressionDepthTrackingMixin,
                   mixins.SubroutinesAsFunctionsMixin):

    bin_depth_threshold = 25

    supported_bin_vector_ops = {
        ast.BinNumOpType.ADD: "add_vectors",
    }

    supported_bin_vector_num_ops = {
        ast.BinNumOpType.MUL: "mul_vector_number",
    }

    exponent_function_name = "exp"
    tanh_function_name = "tanh"

    def __init__(self, indent=4, *args, **kwargs):
        self.indent = indent

        cg = RCodeGenerator(indent=indent)
        super().__init__(None, *args, **kwargs)

    def interpret(self, expr):
        top_cg = self.create_code_generator()

        self.enqueue_subroutine("score", expr)
        self.process_subroutine_queue(top_cg)

        if self.with_linear_algebra:
            filename = os.path.join(
                os.path.dirname(__file__), "linear_algebra.r")
            top_cg.prepend_code_lines(utils.get_file_content(filename))

        return top_cg.code

    def create_code_generator(self):
        return RCodeGenerator(indent=self.indent)

    def interpret_pow_expr(self, expr, **kwargs):
        base_result = self._do_interpret(expr.base_expr, **kwargs)
        exp_result = self._do_interpret(expr.exp_expr, **kwargs)
        return self._cg.infix_expression(
            left=base_result, right=exp_result, op="^")
