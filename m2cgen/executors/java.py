import os
import tempfile
import subprocess


class JavaExecutor:
    def __init__(self, exporter):
        self.exporter = exporter

    def predict(self, X):
        dirpath = tempfile.mkdtemp()

        file_name = os.path.join(dirpath, "{}.java".format(
            self.exporter.model_name))
        code = self.exporter.export(for_validation=True)

        with open(file_name, "w") as f:
            f.write(code)

        subprocess.run(["javac", file_name])

        exec_args = ["java", "-cp", dirpath, self.exporter.model_name] + (
            list(map(str, X[0])))
        result = subprocess.run(exec_args, stdout=subprocess.PIPE)

        return [float(result.stdout)]
