from m2cgen.ast.interpreters.python.interpreter import PythonInterpreter
from m2cgen.exporters.base import BaseExporter


class PythonExporter(BaseExporter):

    def __init__(self, model, model_name="Model", indent=4):
        self.interpreter = PythonInterpreter(
            model_name=model_name,
            indent=indent)
        super(PythonExporter, self).__init__(model)
