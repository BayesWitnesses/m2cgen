import os

from m2cgen import ast
from m2cgen.interpreters import mixins
from m2cgen.interpreters import utils
from m2cgen.interpreters.interpreter import ImperativeToCodeInterpreter
from m2cgen.interpreters.javascript.code_generator \
    import JavascriptCodeGenerator


class JavascriptInterpreter(ImperativeToCodeInterpreter,
                            mixins.LinearAlgebraMixin):

    supported_bin_vector_ops = {
        ast.BinNumOpType.ADD: "addVectors",
    }

    supported_bin_vector_num_ops = {
        ast.BinNumOpType.MUL: "mulVectorNumber",
    }

    abs_function_name = "Math.abs"
    atan_function_name = "Math.atan"
    exponent_function_name = "Math.exp"
    logarithm_function_name = "Math.log"
    log1p_function_name = "Math.log1p"
    power_function_name = "Math.pow"
    sqrt_function_name = "Math.sqrt"
    tanh_function_name = "Math.tanh"

    def __init__(self, indent=4, function_name="score",
                 *args, **kwargs):
        self.indent = indent
        self.function_name = function_name

        cg = JavascriptCodeGenerator(indent=indent)
        super().__init__(cg, *args, **kwargs)

    def interpret(self, expr):
        self._cg.reset_state()
        self._reset_reused_expr_cache()

        args = [self._feature_array_name]

        with self._cg.function_definition(
                name=self.function_name,
                args=args):
            last_result = self._do_interpret(expr)
            self._cg.add_return_statement(last_result)

        if self.with_linear_algebra:
            filename = os.path.join(
                os.path.dirname(__file__), "linear_algebra.js")
            self._cg.add_code_lines(utils.get_file_content(filename))

        return self._cg.finalize_and_get_generated_code()
