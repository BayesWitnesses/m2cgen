import os

from m2cgen import assemblers, interpreters
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

    model_name = "score"

    def __init__(self, model):
        self.model = model
        self.interpreter = interpreters.RInterpreter()

        assembler_cls = assemblers.get_assembler_cls(model)
        self.model_ast = assembler_cls(model).assemble()

        self._r = "Rscript"

    def predict(self, X):
        file_name = os.path.join(self._resource_tmp_dir,
                                 f"{self.model_name}.r")
        exec_args = [self._r,
                     "--vanilla",
                     file_name,
                     *map(utils.format_arg, X)]
        return utils.predict_from_commandline(exec_args)

    def prepare(self):
        executor_code = EXECUTOR_CODE_TPL.format(
            model_code=self.interpreter.interpret(self.model_ast))

        file_name = os.path.join(
            self._resource_tmp_dir, f"{self.model_name}.r")
        with open(file_name, "w") as f:
            f.write(executor_code)
