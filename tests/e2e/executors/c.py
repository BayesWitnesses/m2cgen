import os
import subprocess

from m2cgen import interpreters, assemblers
from tests import utils
from tests.e2e.executors import base


EXECUTOR_CODE_TPL = """
#include <stdio.h>

{model_code}

int main(int argc, char *argv[])
{{
    double input [argc-1];
    for (int i = 1; i < argc; ++i) {{
        sscanf(argv[i], "%lf", &input[i-1]);
    }}

    {print_code}

    return 0;
}}
"""

EXECUTE_AND_PRINT_SCALAR = """
    printf("%f\\n", score(input));
"""

EXECUTE_AND_PRINT_VECTOR_TPL = """
    double result[{size}];
    score(input, result);

    for (int i = 0; i < {size}; ++i) {{
        printf("%f ", *(result+i));
    }}
"""


class CExecutor(base.BaseExecutor):

    model_name = "score"

    def __init__(self, model):
        self.model = model
        self.interpreter = interpreters.CInterpreter()

        assembler_cls = assemblers.get_assembler_cls(model)
        self.model_ast = assembler_cls(model).assemble()

        self._gcc = "gcc"

    def predict(self, X):

        exec_args = [os.path.join(self._resource_tmp_dir, self.model_name)]
        exec_args.extend(map(utils.format_arg, X))
        return utils.predict_from_commandline(exec_args)

    def prepare(self):

        if self.model_ast.output_size > 1:
            print_code = EXECUTE_AND_PRINT_VECTOR_TPL.format(
                size=self.model_ast.output_size)
        else:
            print_code = EXECUTE_AND_PRINT_SCALAR

        executor_code = EXECUTOR_CODE_TPL.format(
            model_code=self.interpreter.interpret(self.model_ast),
            print_code=print_code)

        file_name = os.path.join(
            self._resource_tmp_dir, f"{self.model_name}.c")

        with open(file_name, "w") as f:
            f.write(executor_code)

        target = os.path.join(self._resource_tmp_dir, self.model_name)
        flags = ["-std=c99", "-lm"]
        exec_args = [self._gcc] + [file_name] + ["-o", target] + flags
        subprocess.call(exec_args)
