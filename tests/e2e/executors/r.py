from m2cgen.assemblers import get_assembler_cls
from m2cgen.interpreters import RInterpreter

from tests import utils
from tests.e2e.executors.base import BaseExecutor

EXECUTOR_CODE_TPL = """
args = commandArgs(trailingOnly = TRUE)
input_array <- as.double(args)

{model_code}

res <- score(input_array)
cat(res, sep = " ")
"""


class RExecutor(BaseExecutor):

    def __init__(self, model):
        self.model_name = "score"
        self.model = model
        self.interpreter = RInterpreter()

        assembler_cls = get_assembler_cls(model)
        self.model_ast = assembler_cls(model).assemble()

        self.script_path = None

    def predict(self, X):
        exec_args = [
            "Rscript",
            "--vanilla",
            str(self.script_path),
            *map(utils.format_arg, X)
        ]
        return utils.predict_from_commandline(exec_args)

    def prepare(self):
        executor_code = EXECUTOR_CODE_TPL.format(
            model_code=self.interpreter.interpret(self.model_ast))

        self.script_path = self._resource_tmp_dir / f"{self.model_name}.r"
        utils.write_content_to_file(executor_code, self.script_path)
