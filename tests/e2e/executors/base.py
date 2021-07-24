from contextlib import contextmanager

from tests.utils import tmp_dir


class BaseExecutor:

    _resource_tmp_dir = None

    @contextmanager
    def prepare_then_cleanup(self):
        with tmp_dir() as tmp_dirpath:
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
