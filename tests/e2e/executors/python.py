import sys
from importlib import import_module

from m2cgen import export_to_python

from tests.e2e.executors.base import BaseExecutor
from tests.utils import write_content_to_file


class PythonExecutor(BaseExecutor):

    def __init__(self, model):
        self.model = model

    def predict(self, X):
        # Hacky way to dynamically import generated function

        parent_dir = self._resource_tmp_dir.parent
        package = self._resource_tmp_dir.name

        sys.path.append(str(parent_dir))

        try:
            score = import_module(f"{package}.model").score
        finally:
            sys.path.pop()

        # Use .tolist() since we want to use raw list of floats.
        return score(X.tolist())

    def prepare(self):
        code = export_to_python(self.model)

        file_name = self._resource_tmp_dir / "model.py"
        write_content_to_file(code, file_name)
