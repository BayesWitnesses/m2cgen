import os

from m2cgen import ast
from m2cgen.interpreters import mixins
from m2cgen.interpreters import utils
from m2cgen.interpreters.interpreter import ToCodeInterpreter
from m2cgen.interpreters.javascript.code_generator \
    import JavascriptCodeGenerator


class JavascriptInterpreter(ToCodeInterpreter,
                            mixins.LinearAlgebraMixin):

    supported_bin_vector_ops = {
        ast.BinNumOpType.ADD: "addVectors",
    }

    supported_bin_vector_num_ops = {
        ast.BinNumOpType.MUL: "mulVectorNumber",
    }

    exponent_function_name = "Math.exp"
    power_function_name = "Math.pow"
    tanh_function_name = "Math.tanh"

    def __init__(self, indent=4,
                 *args, **kwargs):
        self.indent = indent

        cg = JavascriptCodeGenerator(indent=indent)
        super(JavascriptInterpreter, self).__init__(cg, *args, **kwargs)

    def interpret(self, expr):
        self._cg.reset_state()
        self._reset_reused_expr_cache()

        args = [self._feature_array_name]

        with self._cg.function_definition(
                name="score",
                args=args):
            last_result = self._do_interpret(expr)
            self._cg.add_return_statement(last_result)

        if self.with_linear_algebra:
            filename = os.path.join(
                os.path.dirname(__file__), "linear_algebra.js")
            self._cg.add_code_lines(utils.get_file_content(filename))

        return self._cg.code
