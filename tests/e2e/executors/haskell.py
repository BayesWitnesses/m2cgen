from m2cgen.assemblers import get_assembler_cls
from m2cgen.interpreters import HaskellInterpreter

from tests import utils
from tests.e2e.executors.base import BaseExecutor

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


class HaskellExecutor(BaseExecutor):

    executor_name = "Main"
    model_name = "Model"

    def __init__(self, model):
        self.model = model
        self.interpreter = HaskellInterpreter()

        assembler_cls = get_assembler_cls(model)
        self.model_ast = assembler_cls(model).assemble()

        self.exec_path = None

    def predict(self, X):
        exec_args = [str(self.exec_path), *map(utils.format_arg, X)]
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

        executor_file_name = self._resource_tmp_dir / f"{self.executor_name}.hs"
        model_file_name = self._resource_tmp_dir / f"{self.model_name}.hs"
        utils.write_content_to_file(executor_code, executor_file_name)
        utils.write_content_to_file(model_code, model_file_name)

        self.exec_path = self._resource_tmp_dir / self.executor_name
        utils.execute_command([
            "ghc",
            str(executor_file_name),
            f"-i{self._resource_tmp_dir}",
            "-o",
            str(self.exec_path)
        ])
