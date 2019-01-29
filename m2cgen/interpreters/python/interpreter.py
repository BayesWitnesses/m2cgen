from m2cgen.interpreters.interpreter import BaseInterpreter
from m2cgen.interpreters.python.code_generator import PythonCodeGenerator


class PythonInterpreter(BaseInterpreter):

    with_linear_algebra = False

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

        if self.with_linear_algebra:
            self._cg.code = "import numpy as np\n" + self._cg.code

        return [
            ("", self._cg.code),
        ]

    def interpret_bin_vector_expr(self, expr):
        self.with_linear_algebra = True
        return "(np.asarray("+self._do_interpret(expr.left)+")" + expr.op.value + "np.asarray("+self._do_interpret(expr.left)+")).tolist()"

    def interpret_bin_vector_num_expr(self, expr):
        self.with_linear_algebra = True
        return "(np.asarray("+self._do_interpret(expr.left)+")" + expr.op.value + self._do_interpret(expr.left) + ").tolist()"

