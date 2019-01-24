import contextlib

from tests import utils


class BaseExecutor:

    _resource_tmp_dir = None

    @contextlib.contextmanager
    def prepare_then_cleanup(self):
        with utils.tmp_dir() as tmp_dirpath:
            self._resource_tmp_dir = tmp_dirpath

            self.prepare()
            yield

    def prepare(self):
        raise NotImplementedError
