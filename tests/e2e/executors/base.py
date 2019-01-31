import contextlib
import subprocess

from tests import utils


class BaseExecutor:

    _resource_tmp_dir = None

    @contextlib.contextmanager
    def prepare_then_cleanup(self):
        with utils.tmp_dir() as tmp_dirpath:
            self._resource_tmp_dir = tmp_dirpath
            self.prepare()

            try:
                yield
            finally:
                self._resource_tmp_dir = None

    def prepare(self):
        raise NotImplementedError

    def _predict_from_commandline(self, exec_args):
        result = subprocess.Popen(exec_args, stdout=subprocess.PIPE)
        items = result.stdout.read().decode("utf-8").strip().split(" ")
        if len(items) == 1:
            return float(items[0])
        else:
            return [float(i) for i in items]
