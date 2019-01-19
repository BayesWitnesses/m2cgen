from m2cgen.ast.interpreters.interpreter import BaseInterpreter
from m2cgen.ast.interpreters.java.code_generator import JavaCodeGenerator


class JavaInterpreter(BaseInterpreter):

    def __init__(self, package_name=None, model_name="Model", indent=4):
        self.package_name = package_name
        self.model_name = model_name
        self.cg = JavaCodeGenerator(indent=indent)

    def interpret(self, expr):
        self.cg.reset_state()

        if self.package_name:
            self.cg.add_package_name(self.package_name)

        with self.cg.class_definition(self.model_name):
            with self.cg.method_definition():
                last_result = self._do_interpret(expr)
                self.cg.add_return_statement(last_result)

        return [
            (self.model_name, self.cg.code),
        ]
