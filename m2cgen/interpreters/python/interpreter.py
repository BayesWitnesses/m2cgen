from m2cgen.interpreters import mixins
from m2cgen.interpreters.interpreter import ToCodeInterpreter
from m2cgen.interpreters.python.code_generator import PythonCodeGenerator


class PythonInterpreter(ToCodeInterpreter,
                        mixins.BinExpressionDepthTrackingMixin,
                        mixins.LinearAlgebraMixin):

    # 60 raises MemoryError for some SVM models with RBF kernel.
    bin_depth_threshold = 55

    exponent_function_name = "math.exp"
    power_function_name = "math.pow"
    tanh_function_name = "math.tanh"

    def __init__(self, indent=4, *args, **kwargs):
        cg = PythonCodeGenerator(indent=indent)
        super(PythonInterpreter, self).__init__(cg, *args, **kwargs)

    def interpret(self, expr):
        self._cg.reset_state()
        self._reset_reused_expr_cache()

        with self._cg.function_definition(
                name="score",
                args=[self._feature_array_name]):
            last_result = self._do_interpret(expr)
            self._cg.add_return_statement(last_result)

        if self.with_math_module:
            self._cg.add_dependency("math")

        if self.with_linear_algebra:
            self._cg.add_dependency("numpy", alias="np")

        return self._cg.code

    def interpret_bin_vector_expr(self, expr, **kwargs):
        self.with_linear_algebra = True
        return self._cg.infix_expression(
            left=self._cg.array_convert_to_numpy(
                self._do_interpret(expr.left, **kwargs)),
            op=expr.op.value,
            right=self._cg.array_convert_to_numpy(
                self._do_interpret(expr.right, **kwargs)))

    def interpret_bin_vector_num_expr(self, expr, **kwargs):
        self.with_linear_algebra = True
        return self._cg.infix_expression(
            left=self._cg.array_convert_to_numpy(
                self._do_interpret(expr.left, **kwargs)),
            op=expr.op.value,
            right=self._do_interpret(expr.right, **kwargs))
