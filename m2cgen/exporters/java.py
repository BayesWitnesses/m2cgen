from m2cgen.ast.interpreters.java import JavaInterpreter
from m2cgen.exporters.base import BaseExporter


class JavaExporter(BaseExporter):

    def __init__(self, model, package_name=None, model_name="Model", indent=4):
        self.interpreter = JavaInterpreter(
            package_name=package_name,
            model_name=model_name,
            indent=indent)
        super(JavaExporter, self).__init__(model)
