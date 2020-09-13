import os

from m2cgen import ast
from m2cgen.interpreters import mixins
from m2cgen.interpreters import utils
from m2cgen.interpreters.interpreter import ImperativeToCodeInterpreter
from m2cgen.interpreters.java.code_generator import JavaCodeGenerator


class JavaInterpreter(ImperativeToCodeInterpreter,
                      mixins.LinearAlgebraMixin,
                      mixins.SubroutinesMixin):

    # The below numbers have been determined experimentally and are subject
    # to adjustments in future.
    ast_size_check_frequency = 100
    ast_size_per_subroutine_threshold = 4600

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

    def __init__(self, package_name=None, class_name="Model", indent=4,
                 function_name="score", *args, **kwargs):
        self.package_name = package_name
        self.class_name = class_name
        self.indent = indent
        self.function_name = function_name

        # We don't provide any code generator as for each subroutine we will
        # create a new one and concatenate their results into top_cg created
        # in .interpret() method.
        super().__init__(None, *args, **kwargs)

    def interpret(self, expr):
        top_cg = self.create_code_generator()

        if self.package_name:
            top_cg.add_package_name(self.package_name)

        with top_cg.class_definition(self.class_name):

            # Since we use SubroutinesMixin, we already have logic
            # of adding methods. We create first subroutine for incoming
            # expression and call `process_subroutine_queue` method.
            self.enqueue_subroutine(self.function_name, expr)
            self.process_subroutine_queue(top_cg)

            if self.with_linear_algebra:
                filename = os.path.join(
                    os.path.dirname(__file__), "linear_algebra.java")
                top_cg.add_code_lines(utils.get_file_content(filename))

        return top_cg.finalize_and_get_generated_code()

    # Required by SubroutinesMixin to create new code generator for
    # each subroutine.
    def create_code_generator(self):
        return JavaCodeGenerator(indent=self.indent)
