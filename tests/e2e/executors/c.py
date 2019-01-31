import os
import string
import subprocess

from tests.e2e.executors import base

import m2cgen as m2c


executor_code_tpl = """
#include <stdio.h>

${code}

int main(int argc, char *argv[])
{
    double input [argc-1];
    for (int i = 1; i < argc; ++i) {
        sscanf(argv[i], "%lf", &input[i-1]);
    }

    printf("%f\\n", score(input));

    return 0;
}
"""


class CExecutor(base.BaseExecutor):

    model_name = "score"

    def __init__(self, model):
        self.model = model

        self._gcc = "gcc"

    def predict(self, X):

        exec_args = [os.path.join(self._resource_tmp_dir, self.model_name)]
        exec_args.extend(map(str, X))
        result = subprocess.Popen(exec_args, stdout=subprocess.PIPE)
        items = result.stdout.read().decode("utf-8").split(" ")
        if len(items) == 1:
            return float(items[0])
        else:
            return [float(i) for i in items]

    def prepare(self):
        code = m2c.export_to_c(self.model)
        code = string.Template(executor_code_tpl).substitute(code=code)

        file_name = os.path.join(
            self._resource_tmp_dir, "{}.c".format(self.model_name))
        with open(file_name, "w") as f:
            f.write(code)

        target = os.path.join(self._resource_tmp_dir, self.model_name)
        exec_args = [self._gcc] + [file_name] + ["-o", target, "-std=c99"]
        subprocess.call(exec_args)
