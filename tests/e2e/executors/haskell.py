import os
import subprocess

from m2cgen import assemblers, interpreters
from tests import utils
from tests.e2e.executors import base

EXECUTOR_CODE_TPL = """
module {executor_name} where
import System.Environment (getArgs)
import {model_name}

main = do
    args <- getArgs
    let inputArray = [read i::Double | i <- args]
    let res = score inputArray
    {print_code}
"""

PRINT_SCALAR = "print res"

PRINT_VECTOR = r"""mapM_ (putStr . \x -> show x ++ " ") res"""


class HaskellExecutor(base.BaseExecutor):

    executor_name = "Main"
    model_name = "Model"

    def __init__(self, model):
        self.model = model
        self.interpreter = interpreters.HaskellInterpreter()

        assembler_cls = assemblers.get_assembler_cls(model)
        self.model_ast = assembler_cls(model).assemble()

        self._ghc = "ghc"

    def predict(self, X):
        app_name = os.path.join(self._resource_tmp_dir,
                                self.executor_name)
        exec_args = [app_name,
                     *map(interpreters.utils.format_float, X)]
        return utils.predict_from_commandline(exec_args)

    def prepare(self):
        if self.model_ast.output_size > 1:
            print_code = PRINT_VECTOR
        else:
            print_code = PRINT_SCALAR
        executor_code = EXECUTOR_CODE_TPL.format(
            executor_name=self.executor_name,
            model_name=self.model_name,
            print_code=print_code)
        model_code = self.interpreter.interpret(self.model_ast)

        executor_file_name = os.path.join(
            self._resource_tmp_dir, f"{self.executor_name}.hs")
        model_file_name = os.path.join(
            self._resource_tmp_dir, f"{self.model_name}.hs")
        with open(executor_file_name, "w") as f:
            f.write(executor_code)
        with open(model_file_name, "w") as f:
            f.write(model_code)

        exec_args = [self._ghc, executor_file_name,
                     f"-i{self._resource_tmp_dir}",
                     "-o", os.path.join(self._resource_tmp_dir,
                                        self.executor_name)]
        subprocess.call(exec_args)
