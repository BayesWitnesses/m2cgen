import os

from py_mini_racer import py_mini_racer

from m2cgen import export_to_javascript
from tests import utils
from tests.e2e.executors.base import BaseExecutor


class JavascriptExecutor(BaseExecutor):

    def __init__(self, model):
        self.model = model

    def predict(self, X):
        file_name = os.path.join(self._resource_tmp_dir, "model.js")

        with open(file_name, 'r') as myfile:
            code = myfile.read()

        args = ",".join(map(utils.format_arg, X))
        caller = f"score([{args}]);\n"

        ctx = py_mini_racer.MiniRacer()
        result = ctx.eval(f"{caller}{code}")

        return result

    def prepare(self):
        code = export_to_javascript(self.model)

        file_name = os.path.join(self._resource_tmp_dir, "model.js")

        with open(file_name, "w") as f:
            f.write(code)
