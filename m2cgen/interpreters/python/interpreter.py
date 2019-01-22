from m2cgen.interpreters.interpreter import BaseInterpreter
from m2cgen.interpreters.python.code_generator import PythonCodeGenerator


class PythonInterpreter(BaseInterpreter):

    def __init__(self, model_name="Model", indent=4, *args, **kwargs):
        self.model_name = model_name
        cg = PythonCodeGenerator(indent=indent)
        super(PythonInterpreter, self).__init__(cg, *args, **kwargs)

    def interpret(self, expr):
        self._cg.reset_state()

        with self._cg.class_definition(self.model_name):
            with self._cg.method_definition(
                    name="score",
                    args=[self._feature_array_name]):
                last_result = self._do_interpret(expr)
                self._cg.add_return_statement(last_result)

        return [
            (self.model_name, self._cg.code),
        ]
