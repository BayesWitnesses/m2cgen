from m2cgen.ast.interpreters.interpreter import BaseInterpreter
from m2cgen.ast.interpreters.java.code_generator import JavaCodeGenerator


class JavaInterpreter(BaseInterpreter):

    def __init__(self, package_name=None, model_name="Model", indent=4,
                 *args, **kwargs):
        self.package_name = package_name
        self.model_name = model_name
        cg = JavaCodeGenerator(indent=indent)
        super(JavaInterpreter, self).__init__(cg, *args, **kwargs)

    def interpret(self, expr):
        self._cg.reset_state()

        if self.package_name:
            self._cg.add_package_name(self.package_name)

        with self._cg.class_definition(self.model_name):
            with self._cg.method_definition(
                    name="score",
                    args=[("double[]", self._feature_array_name)],
                    return_type="double"):
                last_result = self._do_interpret(expr)
                self._cg.add_return_statement(last_result)

        return [
            (self.model_name, self._cg.code),
        ]
