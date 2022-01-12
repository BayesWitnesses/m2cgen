from platform import system

from m2cgen.assemblers import get_assembler_cls
from m2cgen.interpreters import PowershellInterpreter

from tests import utils
from tests.e2e.executors.base import BaseExecutor

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


class PowershellExecutor(BaseExecutor):

    def __init__(self, model):
        self.model_name = "score"
        self.model = model
        self.interpreter = PowershellInterpreter()

        assembler_cls = get_assembler_cls(model)
        self.model_ast = assembler_cls(model).assemble()

        self._powershell = "powershell" if system() == "Windows" else "pwsh"

        self.script_path = None

    def predict(self, X):
        exec_args = [
            self._powershell,
            "-File",
            str(self.script_path),
            "-InputArray",
            ",".join(map(utils.format_arg, X))
        ]
        return utils.predict_from_commandline(exec_args)

    def prepare(self):
        executor_code = EXECUTOR_CODE_TPL.format(
            model_code=self.interpreter.interpret(self.model_ast))

        self.script_path = self._resource_tmp_dir / f"{self.model_name}.ps1"
        utils.write_content_to_file(executor_code, self.script_path)
