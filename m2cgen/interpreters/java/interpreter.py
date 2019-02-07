import os

from m2cgen import ast
from m2cgen.interpreters import mixins
from m2cgen.interpreters import utils
from m2cgen.interpreters.interpreter import ToCodeInterpreter
from m2cgen.interpreters.java.code_generator import JavaCodeGenerator
from m2cgen.interpreters.mixins import Subroutine


class JavaInterpreter(ToCodeInterpreter,
                      mixins.LinearAlgebraMixin,
                      mixins.SubroutinesAsFunctionsMixin):

    supported_bin_vector_ops = {
        ast.BinNumOpType.ADD: "addVectors",
    }

    supported_bin_vector_num_ops = {
        ast.BinNumOpType.MUL: "mulVectorNumber",
    }

    def __init__(self, package_name=None, class_name="Model", indent=4,
                 *args, **kwargs):
        self.package_name = package_name
        self.class_name = class_name
        self.indent = indent

        cg = self.create_code_generator()
        super(JavaInterpreter, self).__init__(cg, *args, **kwargs)

    def interpret(self, expr):
        top_cg = self.create_code_generator()

        if self.package_name:
            top_cg.add_package_name(self.package_name)

        with top_cg.class_definition(self.class_name):

            # Since we use SubroutinesAsFunctionsMixin, we already have logic of
            # adding methods. We create first subroutine for incoming
            # expression and call `interpret_subroutines` method to process it.
            self.subroutine_expr_queue = [Subroutine("score", expr)]
            self.interpret_subroutines(top_cg)

            if self.with_linear_algebra:
                filename = os.path.join(
                    os.path.dirname(__file__), "linear_algebra.java")
                top_cg.add_code_lines(utils.get_file_content(filename))

        return top_cg.code

    # Required by SubroutinesAsFunctionsMixin to create new code generator for
    # new subroutine.
    def create_code_generator(self):
        return JavaCodeGenerator(indent=self.indent)
