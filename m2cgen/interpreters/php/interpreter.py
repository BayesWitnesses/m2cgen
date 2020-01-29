import os

from m2cgen import ast
from m2cgen.interpreters import utils, mixins
from m2cgen.interpreters.php.code_generator import PhpCodeGenerator
from m2cgen.interpreters.interpreter import ToCodeInterpreter


class PhpInterpreter(ToCodeInterpreter, mixins.LinearAlgebraMixin):

    supported_bin_vector_ops = {
        ast.BinNumOpType.ADD: "add_vectors",
    }

    supported_bin_vector_num_ops = {
        ast.BinNumOpType.MUL: "mul_vector_number",
    }

    exponent_function_name = "exp"
    power_function_name = "pow"
    tanh_function_name = "tanh"

    def __init__(self, indent=4, *args, **kwargs):
        cg = PhpCodeGenerator(indent=indent)
        super(PhpInterpreter, self).__init__(cg, *args, **kwargs)

    def interpret(self, expr):
        self._cg.reset_state()
        self._reset_reused_expr_cache()

        with self._cg.function_definition(
                name="score",
                args=[(True, self._feature_array_name)]):
            last_result = self._do_interpret(expr)
            self._cg.add_return_statement(last_result)

        if self.with_linear_algebra:
            filename = os.path.join(
                os.path.dirname(__file__), "linear_algebra.php")
            self._cg.prepend_code_lines(utils.get_file_content(filename))

        self._cg.prepend_code_line("<?php")

        return self._cg.code
