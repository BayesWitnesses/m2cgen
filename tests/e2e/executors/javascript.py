from py_mini_racer import py_mini_racer

from m2cgen import export_to_javascript
from m2cgen.interpreters.utils import get_file_content

from tests import utils
from tests.e2e.executors.base import BaseExecutor


class JavascriptExecutor(BaseExecutor):

    def __init__(self, model):
        self.model = model

        self.script_path = None

    def predict(self, X):
        code = get_file_content(self.script_path)

        args = ",".join(map(utils.format_arg, X))
        caller = f"score([{args}])"

        ctx = py_mini_racer.MiniRacer()
        ctx.eval(code)
        result = ctx.execute(caller)

        return result

    def prepare(self):
        code = export_to_javascript(self.model)

        self.script_path = self._resource_tmp_dir / "model.js"
        utils.write_content_to_file(code, self.script_path)
