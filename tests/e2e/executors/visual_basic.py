import os
import string
import subprocess

from m2cgen import assemblers, interpreters
from tests import utils
from tests.e2e.executors import base

EXECUTOR_CODE_TPL = """
Module Program

    Sub Main(ByVal cmdArgs() As String)
        Dim input_() As Double
        ReDim input_(UBound(cmdArgs) - LBound(cmdArgs))
        Dim i As Integer
        For i = LBound(cmdArgs) To UBound(cmdArgs)
            input_(i) = CDbl(cmdArgs(i))
        Next i
        ${print_code}
    End Sub

End Module
"""

EXECUTE_AND_PRINT_SCALAR = """
        Dim res As Double
        res = score(input_)
        Console.Write(res)
"""

EXECUTE_AND_PRINT_VECTOR = """
        Dim res() As Double
        res = score(input_)
        For i = LBound(res) To UBound(res)
            Console.Write("{0} ", res(i))
        Next i
"""


class VisualBasicExecutor(base.BaseExecutor):

    target_exec_dir = None
    project_name = "test_model"
    _dotnet = "dotnet"

    def __init__(self, model):
        self.model = model
        self.interpreter = interpreters.VisualBasicInterpreter()

        assembler_cls = assemblers.get_assembler_cls(model)
        self.model_ast = assembler_cls(model).assemble()

    def predict(self, X):
        exec_args = [os.path.join(self.target_exec_dir, self.project_name)]
        exec_args.extend(map(str, X))
        return utils.predict_from_commandline(exec_args)

    @classmethod
    def prepare_global(cls):
        super(VisualBasicExecutor, cls).prepare_global()
        if cls.target_exec_dir is None:
            cls.target_exec_dir = os.path.join(cls._global_resource_tmp_dir,
                                               "bin")

            subprocess.call([cls._dotnet,
                             "new",
                             "console",
                             "--output",
                             cls._global_resource_tmp_dir,
                             "--name",
                             cls.project_name,
                             "--language",
                             "VB"])

    def prepare(self):
        if self.model_ast.output_size > 1:
            print_code = EXECUTE_AND_PRINT_VECTOR
        else:
            print_code = EXECUTE_AND_PRINT_SCALAR
        executor_code = string.Template(EXECUTOR_CODE_TPL).substitute(
            print_code=print_code)
        model_code = self.interpreter.interpret(self.model_ast)

        model_file_name = os.path.join(self._global_resource_tmp_dir,
                                       "Model.vb")
        executor_file_name = os.path.join(self._global_resource_tmp_dir,
                                          "Program.vb")
        with open(model_file_name, "w") as f:
            f.write(model_code)
        with open(executor_file_name, "w") as f:
            f.write(executor_code)

        subprocess.call([self._dotnet,
                         "build",
                         os.path.join(self._global_resource_tmp_dir,
                                      "{}.vbproj".format(self.project_name)),
                         "--output",
                         self.target_exec_dir])
