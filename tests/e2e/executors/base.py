import contextlib

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

    @classmethod
    def prepare_global(cls, **kwargs):
        for key, value in kwargs.items():
            setattr(cls, f"_{key}", value)
