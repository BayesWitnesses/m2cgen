from pathlib import Path

from m2cgen.ast import BinNumOpType
from m2cgen.interpreters.interpreter import ImperativeToCodeInterpreter
from m2cgen.interpreters.java.code_generator import JavaCodeGenerator
from m2cgen.interpreters.mixins import LinearAlgebraMixin, PowExprFunctionMixin, SubroutinesMixin
from m2cgen.interpreters.utils import get_file_content


class JavaInterpreter(ImperativeToCodeInterpreter,
                      PowExprFunctionMixin,
                      LinearAlgebraMixin,
                      SubroutinesMixin):

    # The below numbers have been determined experimentally and are subject
    # to adjustments in future.
    ast_size_check_frequency = 100
    ast_size_per_subroutine_threshold = 4600
    subroutine_per_group_threshold = 15

    supported_bin_vector_ops = {
        BinNumOpType.ADD: "addVectors",
    }

    supported_bin_vector_num_ops = {
        BinNumOpType.MUL: "mulVectorNumber",
    }

    abs_function_name = "Math.abs"
    atan_function_name = "Math.atan"
    exponent_function_name = "Math.exp"
    logarithm_function_name = "Math.log"
    log1p_function_name = "Math.log1p"
    power_function_name = "Math.pow"
    sigmoid_function_name = "sigmoid"
    softmax_function_name = "softmax"
    sqrt_function_name = "Math.sqrt"
    tanh_function_name = "Math.tanh"

    with_sigmoid_expr = False
    with_softmax_expr = False

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
            self.enqueue_subroutine(self.function_name, 0, expr)
            self.process_subroutine_queue(top_cg)

            current_dir = Path(__file__).absolute().parent

            if self.with_linear_algebra:
                filename = current_dir / "linear_algebra.java"
                top_cg.add_code_lines(get_file_content(filename))

            if self.with_softmax_expr:
                filename = current_dir / "softmax.java"
                top_cg.add_code_lines(get_file_content(filename))

            if self.with_sigmoid_expr:
                filename = current_dir / "sigmoid.java"
                top_cg.add_code_lines(get_file_content(filename))

        return top_cg.finalize_and_get_generated_code()

    # Required by SubroutinesMixin to create new code generator for
    # each subroutine.
    def create_code_generator(self):
        return JavaCodeGenerator(indent=self.indent)

    def interpret_softmax_expr(self, expr, **kwargs):
        self.with_softmax_expr = True
        return super().interpret_softmax_expr(expr, **kwargs)

    def interpret_sigmoid_expr(self, expr, **kwargs):
        self.with_sigmoid_expr = True
        return super().interpret_sigmoid_expr(expr, **kwargs)
