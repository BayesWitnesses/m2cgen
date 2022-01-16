import subprocess

from m2cgen.assemblers import get_assembler_cls
from m2cgen.interpreters import ElixirInterpreter

from tests import utils
from tests.e2e.executors.base import BaseExecutor

EXECUTOR_CODE_TPL = """
{model_code}

defmodule Runner do
    def run do
        input = Enum.map(System.argv, fn x -> Float.parse(x) |> elem(0) end)
        res = Model.score(input)


        if is_list(res) do
            res
            |> Enum.map(fn x -> to_string(x) end)
            |> Enum.join(" ")
            |> IO.puts
        else
            to_string(res)
            |> IO.puts
        end
    end
end
"""


class ElixirExecutor(BaseExecutor):

    def __init__(self, model):
        self.model_name = "score"
        self.model = model
        self.interpreter = ElixirInterpreter()

        assembler_cls = get_assembler_cls(model)
        self.model_ast = assembler_cls(model).assemble()

        self.exec_path = None

    def predict(self, X):
        exec_args = [
            "elixir",
            "-pz",
            self.exec_path,
            "-e",
            "Elixir.Runner.run",
            *map(utils.format_arg, X)
        ]

        return utils.predict_from_commandline(exec_args)

    def prepare(self):
        executor_code = EXECUTOR_CODE_TPL.format(
            model_code=self.interpreter.interpret(self.model_ast))

        self.exec_path = self._resource_tmp_dir
        script_path = self._resource_tmp_dir / f"{self.model_name}.ex"

        utils.write_content_to_file(executor_code, script_path)

        subprocess.call([
            "elixirc",
            "-o",
            self.exec_path,
            str(script_path)
        ])
