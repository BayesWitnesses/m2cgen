import os
import math

from m2cgen import ast
from m2cgen.interpreters import mixins
from m2cgen.interpreters import utils
from m2cgen.interpreters.interpreter import ToCodeInterpreter
from m2cgen.interpreters.java.code_generator import JavaCodeGenerator


class JavaInterpreter(ToCodeInterpreter,
                      mixins.LinearAlgebraMixin,
                      mixins.SubroutinesAsFunctionsMixin,
                      mixins.BinExpressionDepthTrackingMixin):

    # The below numbers have been determined experimentally and are subject
    # to adjustments in future.
    bin_depth_threshold = 100
    ast_size_per_subroutine_threshold = 4600

    supported_bin_vector_ops = {
        ast.BinNumOpType.ADD: "addVectors",
    }

    supported_bin_vector_num_ops = {
        ast.BinNumOpType.MUL: "mulVectorNumber",
    }

    exponent_function_name = "Math.exp"
    power_function_name = "Math.pow"
    tanh_function_name = "Math.tanh"

    def __init__(self, package_name=None, class_name="Model", indent=4,
                 *args, **kwargs):
        self.package_name = package_name
        self.class_name = class_name
        self.indent = indent

        # We don't provide any code generator as for each subroutine we will
        # create a new one and concatenate their results into top_cg created
        # in .interpret() method.
        super().__init__(None, *args, **kwargs)

    def interpret(self, expr):
        top_cg = self.create_code_generator()

        if self.package_name:
            top_cg.add_package_name(self.package_name)

        with top_cg.class_definition(self.class_name):

            # Since we use SubroutinesAsFunctionsMixin, we already have logic
            # of adding methods. We create first subroutine for incoming
            # expression and call `process_subroutine_queue` method.
            self.enqueue_subroutine("score", expr)
            self.process_subroutine_queue(top_cg)

            if self.with_linear_algebra:
                filename = os.path.join(
                    os.path.dirname(__file__), "linear_algebra.java")
                top_cg.add_code_lines(utils.get_file_content(filename))

        return top_cg.code

    def interpret_subroutine_expr(self, expr, **kwargs):
        return self._do_interpret(expr.expr, **kwargs)

    # Required by SubroutinesAsFunctionsMixin to create new code generator for
    # each subroutine.
    def create_code_generator(self):
        return JavaCodeGenerator(indent=self.indent)

    def bin_depth_threshold_hook(self, expr, **kwargs):
        # The condition below is a sanity check to ensure that the expression
        # is actually worth moving into a separate subroutine.
        if ast.count_exprs(expr) > self.ast_size_per_subroutine_threshold:
            function_name = self._get_subroutine_name()
            self.enqueue_subroutine(function_name, expr)
            return self._cg.function_invocation(
                function_name, self._feature_array_name)
        else:
            return self._do_interpret(expr, **kwargs)

    def _pre_interpret_hook(self, expr, **kwargs):
        if isinstance(expr, ast.BinExpr):
            threshold = self._calc_bin_depth_threshold(expr)
            self.bin_depth_threshold = min(threshold, self.bin_depth_threshold)
        return super()._pre_interpret_hook(expr, **kwargs)

    def _calc_bin_depth_threshold(self, expr):
        # The logic below counts the number of non-binary expressions
        # in a non-recursive branch of a binary expression to account
        # for large tree-like models and adjust the bin depth threshold
        # if necessary.
        cnt = None
        if not isinstance(expr.left, ast.BinExpr):
            cnt = ast.count_exprs(expr.left, exclude_list={ast.BinExpr})
        elif not isinstance(expr.right, ast.BinExpr):
            cnt = ast.count_exprs(expr.right, exclude_list={ast.BinExpr})
        if cnt and cnt < self.ast_size_per_subroutine_threshold:
            return math.ceil(self.ast_size_per_subroutine_threshold / cnt)
        return self.bin_depth_threshold
