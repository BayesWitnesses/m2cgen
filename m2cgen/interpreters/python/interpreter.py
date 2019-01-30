from m2cgen.interpreters.interpreter import BaseInterpreter
from m2cgen.interpreters.python.code_generator import PythonCodeGenerator


class PythonInterpreter(BaseInterpreter):

    with_vectors = False

    def __init__(self, indent=4, *args, **kwargs):
        cg = PythonCodeGenerator(indent=indent)
        super(PythonInterpreter, self).__init__(cg, *args, **kwargs)

    def interpret(self, expr):
        self._cg.reset_state()

        with self._cg.function_definition(
                name="score",
                args=[self._feature_array_name]):
            last_result = self._do_interpret(expr)
            self._cg.add_return_statement(last_result)

        if self.with_vectors:
            self._cg.add_dependency("numpy", alias="np")

        return [
            ("", self._cg.code),
        ]

    def interpret_vector_val(self, expr, **kwargs):
        self.with_vectors = True
        return super().interpret_vector_val(expr, **kwargs)

    def interpret_bin_vector_expr(self, expr):
        self.with_vectors = True
        return self._cg.infix_expression(
            left=self._do_interpret(expr.left),
            op=expr.op.value,
            right=self._do_interpret(expr.right))

    def interpret_bin_vector_num_expr(self, expr):
        self.with_vectors = True
        return self._cg.infix_expression(
            left=self._do_interpret(expr.left),
            op=expr.op.value,
            right=self._do_interpret(expr.right))
