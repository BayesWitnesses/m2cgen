from m2cgen.interpreters.interpreter import BaseInterpreter
from m2cgen.interpreters.c.code_generator import CCodeGenerator


class CInterpreter(BaseInterpreter):

    def __init__(self, indent=4, *args, **kwargs):
        cg = CCodeGenerator(indent=indent)
        super(CInterpreter, self).__init__(cg, *args, **kwargs)

    def interpret(self, expr):
        self._cg.reset_state()

        with self._cg.function_definition(
                name="score",
                args=[(True, self._feature_array_name)],
                is_vector_output=expr.is_vector_output):
            last_result = self._do_interpret(expr)
            self._cg.add_return_statement(last_result)

        return self._cg.code
