import os

from m2cgen import ast
from m2cgen.interpreters import mixins
from m2cgen.interpreters import utils
from m2cgen.interpreters.interpreter import ToCodeInterpreter
from m2cgen.interpreters.javascript.code_generator \
    import JavascriptCodeGenerator


class JavascriptInterpreter(ToCodeInterpreter,
                            mixins.LinearAlgebraMixin,
                            mixins.SubroutinesAsFunctionsMixin):

    supported_bin_vector_ops = {
        ast.BinNumOpType.ADD: "addVectors",
    }

    supported_bin_vector_num_ops = {
        ast.BinNumOpType.MUL: "mulVectorNumber",
    }

    exponent_function_name = "Math.exp"
    power_function_name = "Math.pow"
    tanh_function_name = "Math.tanh"

    def __init__(self, with_util_functions=False, indent=4,
                 *args, **kwargs):
        self.indent = indent
        self.with_util_functions = with_util_functions

        # We don't provide any code generator as for each subroutine we will
        # create a new one and concatenate their results into top_cg created
        # in .interpret() method.
        super().__init__(None, *args, **kwargs)

    def interpret(self, expr):
        top_cg = self.create_code_generator()

        # Since we use SubroutinesAsFunctionsMixin, we already have logic
        # of adding methods. We create first subroutine for incoming
        # expression and call `process_subroutine_queue` method.
        self.enqueue_subroutine("score", expr)
        self.process_subroutine_queue(top_cg)

        if self.with_util_functions:
            utils_filename = os.path.join(
                os.path.dirname(__file__), "utils.js")
            top_cg.add_code_lines(utils.get_file_content(utils_filename))

        if self.with_linear_algebra:
            filename = os.path.join(
                os.path.dirname(__file__), "linear_algebra.js")
            top_cg.add_code_lines(utils.get_file_content(filename))

        return top_cg.code

    # Required by SubroutinesAsFunctionsMixin to create new code generator for
    # each subroutine.
    def create_code_generator(self):
        return JavascriptCodeGenerator(indent=self.indent)
