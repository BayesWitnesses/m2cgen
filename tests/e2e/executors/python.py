import importlib
import os
import sys

from m2cgen import exporters
from tests.e2e.executors import base


class PythonExecutor(base.BaseExecutor):

    def __init__(self, model):
        self.model = model
        self.exporter = exporters.PythonExporter(model)

    def predict(self, X):
        # Hacky way to dynamically import generated function

        parent_dir = os.path.dirname(self._resource_tmp_dir)
        package = os.path.basename(self._resource_tmp_dir)

        sys.path.append(parent_dir)

        try:
            score = importlib.import_module("{}.model".format(package)).score
        finally:
            sys.path.pop()

        # Use .tolist() since we want to use raw list of floats.
        return score(X.tolist())

    def prepare(self):
        exported_models = self.exporter.export()
        assert len(exported_models) == 1

        _, code = exported_models[0]

        file_name = os.path.join(self._resource_tmp_dir, "model.py")
        print(file_name)

        with open(file_name, "w") as f:
            f.write(code)
