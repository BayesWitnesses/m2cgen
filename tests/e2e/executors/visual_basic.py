from m2cgen.assemblers import get_assembler_cls
from m2cgen.interpreters import VisualBasicInterpreter

from tests import utils
from tests.e2e.executors.base import BaseExecutor

EXECUTOR_CODE_TPL = """
Module Program

    Sub Main(ByVal cmdArgs() As String)
        Dim inputVector() As Double
        ReDim inputVector(UBound(cmdArgs) - LBound(cmdArgs))
        Dim i As Integer
        For i = LBound(cmdArgs) To UBound(cmdArgs)
            inputVector(i) = CDbl(cmdArgs(i))
        Next i
        {print_code}
    End Sub

End Module
"""

EXECUTE_AND_PRINT_SCALAR = """
        Dim res As Double
        res = Score(inputVector)
        Console.Write(res)
"""

EXECUTE_AND_PRINT_VECTOR = """
        Dim res() As Double
        res = Score(inputVector)
        For i = LBound(res) To UBound(res)
            Console.Write("{0} ", res(i))
        Next i
"""


class VisualBasicExecutor(BaseExecutor):

    target_exec_dir = None
    project_name = "test_model"

    def __init__(self, model):
        self.model = model
        self.interpreter = VisualBasicInterpreter()

        assembler_cls = get_assembler_cls(model)
        self.model_ast = assembler_cls(model).assemble()

    def predict(self, X):
        exec_args = [
            str(self.target_exec_dir / self.project_name),
            *map(utils.format_arg, X)
        ]
        return utils.predict_from_commandline(exec_args)

    @classmethod
    def prepare_global(cls, **kwargs):
        super().prepare_global(**kwargs)
        if cls.target_exec_dir is None:
            cls.target_exec_dir = cls._global_tmp_dir / "bin"
            utils.execute_command([
                "dotnet",
                "new",
                "console",
                "--output",
                str(cls._global_tmp_dir),
                "--name",
                cls.project_name,
                "--language",
                "VB"
            ])

    def prepare(self):
        if self.model_ast.output_size > 1:
            print_code = EXECUTE_AND_PRINT_VECTOR
        else:
            print_code = EXECUTE_AND_PRINT_SCALAR
        executor_code = EXECUTOR_CODE_TPL.format(
            print_code=print_code)
        model_code = self.interpreter.interpret(self.model_ast)

        model_file_name = self._global_tmp_dir / "Model.vb"
        executor_file_name = self._global_tmp_dir / "Program.vb"
        utils.write_content_to_file(model_code, model_file_name)
        utils.write_content_to_file(executor_code, executor_file_name)

        utils.execute_command([
            "dotnet",
            "build",
            str(self._global_tmp_dir / f"{self.project_name}.vbproj"),
            "--output",
            str(self.target_exec_dir)
        ])
