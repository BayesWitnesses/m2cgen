from m2cgen.assemblers import get_assembler_cls
from m2cgen.interpreters import GoInterpreter

from tests import utils
from tests.e2e.executors.base import BaseExecutor

EXECUTOR_CODE_TPL = """
package main

import (
    "fmt"
    "os"
    "strconv"
)

{model_code}

func main() {{
    input := make([]float64, 0, len(os.Args)-1)
    for _, s := range os.Args[1:] {{
        f, _ := strconv.ParseFloat(s, 64)
        input = append(input, f)
    }}

    {print_code}
}}
"""

EXECUTE_AND_PRINT_SCALAR = """
    fmt.Printf("%f\\n", score(input))
"""

EXECUTE_AND_PRINT_VECTOR = """
    result := score(input)

    for _, v := range result {
        fmt.Printf("%f ", v)
    }
"""


class GoExecutor(BaseExecutor):

    def __init__(self, model):
        self.model_name = "score"
        self.model = model
        self.interpreter = GoInterpreter()

        assembler_cls = get_assembler_cls(model)
        self.model_ast = assembler_cls(model).assemble()

        self.exec_path = None

    def predict(self, X):
        exec_args = [str(self.exec_path), *map(utils.format_arg, X)]
        return utils.predict_from_commandline(exec_args)

    def prepare(self):
        if self.model_ast.output_size > 1:
            print_code = EXECUTE_AND_PRINT_VECTOR
        else:
            print_code = EXECUTE_AND_PRINT_SCALAR

        executor_code = EXECUTOR_CODE_TPL.format(
            model_code=self.interpreter.interpret(self.model_ast),
            print_code=print_code)

        file_name = self._resource_tmp_dir / f"{self.model_name}.go"
        utils.write_content_to_file(executor_code, file_name)

        self.exec_path = self._resource_tmp_dir / self.model_name
        utils.execute_command([
            "go",
            "build",
            "-o",
            str(self.exec_path),
            str(file_name)
        ])
