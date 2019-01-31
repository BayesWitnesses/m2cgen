import os
import string
import subprocess

from m2cgen import interpreters, assemblers
from tests.e2e.executors import base


EXECUTOR_CODE_TPL = """
#include <stdio.h>
#include <string.h>

${model_code}

int main(int argc, char *argv[])
{
    double input [argc-1];
    for (int i = 1; i < argc; ++i) {
        sscanf(argv[i], "%lf", &input[i-1]);
    }

    ${print_code}

    return 0;
}
"""

EXECUTE_AND_PRINT_SCALAR = """
    printf("%f\\n", score(input));
"""

EXECUTE_AND_PRINT_VECTOR_TPL = """
    double *result = score(input);

    for (int i = 0; i < ${size}; ++i) {
        printf("%f ", *(result+i));
    }
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
        exec_args.extend(map(str, X))
        result = subprocess.Popen(exec_args, stdout=subprocess.PIPE)
        items = result.stdout.read().decode("utf-8").strip().split(" ")
        if len(items) == 1:
            return float(items[0])
        else:
            return [float(i) for i in items]

    def prepare(self):

        if self.model_ast.is_vector_output:
            print_code = (
                string.Template(EXECUTE_AND_PRINT_VECTOR_TPL).substitute(
                    size=self.model_ast.size))
        else:
            print_code = EXECUTE_AND_PRINT_SCALAR

        execute_code = string.Template(EXECUTOR_CODE_TPL).substitute(
            model_code=self.interpreter.interpret(self.model_ast),
            print_code=print_code)

        file_name = os.path.join(
            self._resource_tmp_dir, "{}.c".format(self.model_name))

        with open(file_name, "w") as f:
            f.write(execute_code)

        target = os.path.join(self._resource_tmp_dir, self.model_name)
        exec_args = [self._gcc] + [file_name] + ["-o", target, "-std=c99"]
        subprocess.call(exec_args)
