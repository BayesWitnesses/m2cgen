from m2cgen.ast.interpreters.java import JavaInterpreter
from m2cgen.code_generators.java import JavaCodeGenerator
from m2cgen.exporters.base import BaseExporter
from m2cgen.executors.java import JavaExecutor


class JavaExporter(BaseExporter):

    executor_cls = JavaExecutor

    def __init__(self, model, package_name=None, model_name="Model", indent=4):
        self.package_name = package_name
        self.model_name = model_name
        self.code_generator = JavaCodeGenerator(indent=indent)
        super(JavaExporter, self).__init__(model)

    def export_from_ast(self, model_ast, for_validation=False):
        interpreter = JavaInterpreter(self.code_generator)

        if self.package_name:
            self.code_generator.add_package_name(self.package_name)

        with self.code_generator.class_definition(self.model_name):
            with self.code_generator.method_definition():
                interpreter.interpret(model_ast)

            if for_validation:
                self.code_generator.add_raw_method_code("java_main.java.txt")
