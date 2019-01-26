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

    def predict(self, X):
        assert all(map(lambda x: isinstance(x, float), X)), (
            "Only list of floats is acceptable.")
        return self._predict(X)

    def _predict(self, X):
        raise NotImplementedError
