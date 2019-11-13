import contextlib

from tests import utils


class BaseExecutor:

    _resource_tmp_dir = None
    _global_resource_tmp_dir = None

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

    @classmethod
    def prepare_global(cls):
        if cls._global_resource_tmp_dir is None:
            with utils.tmp_dir() as tmp_dirpath:
                cls._global_resource_tmp_dir = tmp_dirpath
