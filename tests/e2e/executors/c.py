import os
import string
import subprocess

from m2cgen import exporters
from tests.e2e.executors import base


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
        self.exporter = exporters.CExporter(model)

        self._gcc = "gcc"

    def predict(self, X):

        exec_args = [os.path.join(self._resource_tmp_dir, self.model_name)]
        exec_args.extend(map(str, X))
        result = subprocess.run(exec_args, stdout=subprocess.PIPE)
        items = result.stdout.decode("utf-8").split(" ")
        if len(items) == 1:
            return float(items[0])
        else:
            return [float(i) for i in items]

    def prepare(self):
        # Create files generated by exporter in the temp dir.
        files_to_compile = []

        for _, code in self.exporter.export():
            file_name = os.path.join(self._resource_tmp_dir,
                                     "{}.cpp".format(self.model_name))

            code = string.Template(executor_code_tpl).substitute(code=code)

            with open(file_name, "w") as f:
                f.write(code)

            files_to_compile.append(file_name)

        assert len(files_to_compile) == 1

        target = os.path.join(self._resource_tmp_dir, self.model_name)
        exec_args = [self._gcc] + files_to_compile + (
            ["-o", target, "-std=c++11"])
        subprocess.call(exec_args)
