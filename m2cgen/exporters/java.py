from m2cgen.ast.interpreters.java import JavaInterpreter
from m2cgen.code_generators.java import JavaCodeGenerator
from m2cgen.exporters.base import BaseExporter


class JavaExporter(BaseExporter):

    def __init__(self, model, package_name=None, model_name="Model", indent=4):
        self.package_name = package_name
        self.model_name = model_name
        self.code_generator = JavaCodeGenerator(indent=indent)
        super(JavaExporter, self).__init__(model)

    def export_from_ast(self, model_ast):
        interpreter = JavaInterpreter(self.code_generator)

        if self.package_name:
            self.code_generator.add_package_name(self.package_name)

        with self.code_generator.class_definition(self.model_name):
            with self.code_generator.method_definition():
                interpreter.interpret(model_ast)
