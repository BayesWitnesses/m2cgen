import importlib
import os
import tempfile
import sys

from m2cgen import exporters


class PythonExecutor:

    def __init__(self, model):
        self.model = model
        self.exporter = exporters.PythonExporter(model)

    def predict(self, X):
        dirpath = tempfile.mkdtemp()

        exported_models = self.exporter.export()
        assert len(exported_models) == 1

        _, code = exported_models[0]

        file_name = os.path.join(dirpath, "model.py")

        with open(file_name, "w") as f:
            f.write(code)

        # Hacky way to dynamically import generated function

        parent_dir = os.path.dirname(dirpath)
        package = os.path.basename(dirpath)

        sys.path.append(parent_dir)

        try:
            score = importlib.import_module("{}.model".format(package)).score
        finally:
            sys.path.pop()

        return score(X)
