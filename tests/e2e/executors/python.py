from m2cgen.assemblers import get_assembler_cls
from m2cgen.interpreters import PythonInterpreter

from tests.e2e.executors.base import BaseExecutor
from tests.utils import write_content_to_file


class PythonExecutor(BaseExecutor):

    def __init__(self, model):
        self.model_name = "score"
        self.model = model
        self.interpreter = PythonInterpreter()

        assembler_cls = get_assembler_cls(model)
        self.model_ast = assembler_cls(model).assemble()

        self.script_path = None

    def predict(self, X):
        scope = {}
        exec(compile(self.script_path.read_bytes(), self.script_path, mode='exec'), scope)

        # Use .tolist() since we want to use raw list of floats.
        return scope['score'](X.tolist())

    def prepare(self):
        model_code = self.interpreter.interpret(self.model_ast)

        self.script_path = self._resource_tmp_dir / f"{self.model_name}.py"
        write_content_to_file(model_code, self.script_path)
