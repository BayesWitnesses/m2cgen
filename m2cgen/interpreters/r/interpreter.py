import os

from m2cgen import ast
from m2cgen.interpreters import mixins, utils
from m2cgen.interpreters.interpreter import ToCodeInterpreter
from m2cgen.interpreters.r.code_generator import RCodeGenerator


class RInterpreter(ToCodeInterpreter, mixins.LinearAlgebraMixin):

    supported_bin_vector_ops = {
        ast.BinNumOpType.ADD: "add_vectors",
    }

    supported_bin_vector_num_ops = {
        ast.BinNumOpType.MUL: "mul_vector_number",
    }

    exponent_function_name = "exp"
    tanh_function_name = "tanh"

    def __init__(self, indent=4, *args, **kwargs):
        cg = RCodeGenerator(indent=indent)
        super(RInterpreter, self).__init__(cg, *args, **kwargs)

    def interpret(self, expr):
        self._cg.reset_state()
        self._reset_reused_expr_cache()

        with self._cg.function_definition(
                name="score",
                args=[self._feature_array_name]):
            last_result = self._do_interpret(expr)
            self._cg.add_return_statement(last_result)

        if self.with_linear_algebra:
            filename = os.path.join(
                os.path.dirname(__file__), "linear_algebra.r")
            self._cg.prepend_code_lines(utils.get_file_content(filename))

        return self._cg.code

    def interpret_pow_expr(self, expr, **kwargs):
        base_result = self._do_interpret(expr.base_expr, **kwargs)
        exp_result = self._do_interpret(expr.exp_expr, **kwargs)
        return self._cg.infix_expression(
            left=base_result, right=exp_result, op="^")
