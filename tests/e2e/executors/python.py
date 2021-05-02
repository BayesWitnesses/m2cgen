import importlib
import os
import sys

from m2cgen import export_to_python
from tests.e2e.executors.base import BaseExecutor


class PythonExecutor(BaseExecutor):

    def __init__(self, model):
        self.model = model

    def predict(self, X):
        # Hacky way to dynamically import generated function

        parent_dir = os.path.dirname(self._resource_tmp_dir)
        package = os.path.basename(self._resource_tmp_dir)

        sys.path.append(parent_dir)

        try:
            score = importlib.import_module(f"{package}.model").score
        finally:
            sys.path.pop()

        # Use .tolist() since we want to use raw list of floats.
        return score(X.tolist())

    def prepare(self):
        code = export_to_python(self.model)

        file_name = os.path.join(self._resource_tmp_dir, "model.py")
        with open(file_name, "w") as f:
            f.write(code)
