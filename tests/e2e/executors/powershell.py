import os
import platform

from m2cgen import assemblers, interpreters
from tests import utils
from tests.e2e.executors import base

EXECUTOR_CODE_TPL = """
param (
    $InputArray
)
$InputArray = [double[]]($InputArray -Split ',')

{model_code}

Score $InputArray | ForEach-Object {{
  Write-Host -NoNewline "$_ "
}}
"""


class PowershellExecutor(base.BaseExecutor):
    model_name = "score"

    def __init__(self, model):
        self.model = model
        self.interpreter = interpreters.PowershellInterpreter()

        assembler_cls = assemblers.get_assembler_cls(model)
        self.model_ast = assembler_cls(model).assemble()

        self._powershell = ("powershell"
                            if platform.system() in ('Windows', 'Microsoft')
                            else "pwsh")

    def predict(self, X):
        file_name = os.path.join(self._resource_tmp_dir,
                                 f"{self.model_name}.ps1")
        exec_args = [self._powershell,
                     "-File",
                     file_name,
                     "-InputArray",
                     ",".join(map(utils.format_arg, X))]
        return utils.predict_from_commandline(exec_args)

    def prepare(self):
        executor_code = EXECUTOR_CODE_TPL.format(
            model_code=self.interpreter.interpret(self.model_ast))

        file_name = os.path.join(
            self._resource_tmp_dir, f"{self.model_name}.ps1")
        with open(file_name, "w") as f:
            f.write(executor_code)
