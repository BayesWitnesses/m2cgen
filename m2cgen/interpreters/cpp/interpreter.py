from m2cgen.interpreters.interpreter import BaseInterpreter
from m2cgen.interpreters.cpp.code_generator import CPPCodeGenerator


class CPPInterpreter(BaseInterpreter):

    def __init__(self, indent=4, *args, **kwargs):
        cg = CPPCodeGenerator(indent=indent)
        super(CPPInterpreter, self).__init__(cg, *args, **kwargs)

    def interpret(self, expr):
        self._cg.reset_state()

        with self._cg.function_definition(
                name="score",
                args=[(True, self._feature_array_name)],
                is_vector_output=expr.is_vector_output):
            last_result = self._do_interpret(expr)
            self._cg.add_return_statement(last_result)

        return [
            ("", self._cg.code),
        ]
