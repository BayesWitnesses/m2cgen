from m2cgen.interpreters import mixins
from m2cgen.interpreters.interpreter import ToCodeInterpreter
from m2cgen.interpreters.python.code_generator import PythonCodeGenerator


class PythonInterpreter(ToCodeInterpreter,
                        mixins.BinExpressionDepthTrackingMixin):

    # 93 may raise MemoryError, so use something close enough to it not to
    # create unnecessary overhead.
    bin_depth_threshold = 80

    def __init__(self, indent=4, *args, **kwargs):
        cg = PythonCodeGenerator(indent=indent)
        super(PythonInterpreter, self).__init__(cg, *args, **kwargs)
        self.with_exponent = False

    def interpret(self, expr):
        self._cg.reset_state()
        self._reset_reused_expr_cache()

        with self._cg.function_definition(
                name="score",
                args=[self._feature_array_name]):
            last_result = self._do_interpret(expr)
            self._cg.add_return_statement(last_result)

        if self.with_vectors or self.with_exponent:
            self._cg.add_dependency("numpy", alias="np")

        return self._cg.code

    def interpret_bin_vector_expr(self, expr, **kwargs):
        return self._cg.infix_expression(
            left=self._do_interpret(expr.left, **kwargs),
            op=expr.op.value,
            right=self._do_interpret(expr.right, **kwargs))

    def interpret_bin_vector_num_expr(self, expr, **kwargs):
        return self._cg.infix_expression(
            left=self._do_interpret(expr.left, **kwargs),
            op=expr.op.value,
            right=self._do_interpret(expr.right, **kwargs))

    def interpret_exp_expr(self, expr):
        self.with_exponent = True
        nested_result = self._do_interpret(expr.expr)
        return self._cg.function_invocation("np.exp", nested_result)
