from m2cgen.assemblers import get_assembler_cls
from m2cgen.interpreters import FSharpInterpreter

from tests import utils
from tests.e2e.executors.base import BaseExecutor

EXECUTOR_CODE_TPL = """
{model_code}

[<EntryPoint>]
let main args =
    let res = score (List.ofSeq (Seq.map double args))
    {print_code}
    0
"""

PRINT_SCALAR = """printf "%f" res"""

PRINT_VECTOR = """res |> List.iter (printf "%f ")"""


class FSharpExecutor(BaseExecutor):

    target_exec_dir = None
    project_name = "test_model"

    def __init__(self, model):
        self.model = model
        self.interpreter = FSharpInterpreter()

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
                "F#"
            ])

    def prepare(self):
        if self.model_ast.output_size > 1:
            print_code = PRINT_VECTOR
        else:
            print_code = PRINT_SCALAR

        code = EXECUTOR_CODE_TPL.format(
            print_code=print_code,
            model_code=self.interpreter.interpret(self.model_ast))

        file_name = self._global_tmp_dir / "Program.fs"
        utils.write_content_to_file(code, file_name)

        utils.execute_command([
            "dotnet",
            "build",
            str(self._global_tmp_dir / f"{self.project_name}.fsproj"),
            "--output",
            str(self.target_exec_dir)
        ])
