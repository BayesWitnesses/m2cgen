from m2cgen.assemblers import get_assembler_cls
from m2cgen.interpreters import CSharpInterpreter

from tests import utils
from tests.e2e.executors.base import BaseExecutor

EXECUTOR_CODE_TPL = """
using System;

namespace TestConsoleApp {{
    class Program {{
        static void Main(string[] args) {{
            double[] input_ = new double[args.Length];
            for(int i = 0; i < input_.Length; ++i) {{
                input_[i] = double.Parse(args[i]);
            }}
            {print_code}
        }}
    }}
}}
"""

EXECUTE_AND_PRINT_SCALAR = """
            double res = ML.Model.Score(input_);
            Console.Write(res);
"""

EXECUTE_AND_PRINT_VECTOR = """
            double[] res = ML.Model.Score(input_);
            for(int i = 0; i < res.Length; ++i) {
                Console.Write("{0} ", res[i]);
            }
"""


class CSharpExecutor(BaseExecutor):

    target_exec_dir = None
    project_name = "test_model"

    def __init__(self, model):
        self.model = model
        self.interpreter = CSharpInterpreter()

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
                "C#"
            ])

    def prepare(self):
        if self.model_ast.output_size > 1:
            print_code = EXECUTE_AND_PRINT_VECTOR
        else:
            print_code = EXECUTE_AND_PRINT_SCALAR
        executor_code = EXECUTOR_CODE_TPL.format(
            print_code=print_code)
        model_code = self.interpreter.interpret(self.model_ast)

        model_file_name = self._global_tmp_dir / "Model.cs"
        executor_file_name = self._global_tmp_dir / "Program.cs"
        utils.write_content_to_file(model_code, model_file_name)
        utils.write_content_to_file(executor_code, executor_file_name)

        utils.execute_command([
            "dotnet",
            "build",
            str(self._global_tmp_dir / f"{self.project_name}.csproj"),
            "--output",
            str(self.target_exec_dir)
        ])
