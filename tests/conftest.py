import io
import pickle

import pytest
from sklearn.linear_model import LinearRegression

from tests.utils import get_regression_model_trainer, tmp_dir


def pytest_addoption(parser):
    parser.addoption(
        "--fast", action="store_const",
        default=False, const=True, help="Run e2e tests fast"
    )


@pytest.fixture
def is_fast(request):
    return request.config.getoption("--fast")


@pytest.fixture(scope="module")
def global_tmp_dir():
    with tmp_dir() as directory:
        yield directory


@pytest.fixture(scope="module")
def trained_model():
    estimator = LinearRegression()
    return get_regression_model_trainer()(estimator)[2]


@pytest.fixture
def pickled_model(trained_model):
    infile = io.BytesIO()
    pickle.dump(trained_model, infile)
    infile.seek(0)
    return infile


@pytest.fixture(scope="module")
def path_to_pickled_model(global_tmp_dir, trained_model):
    p = global_tmp_dir / "model.pickle"
    p.write_bytes(pickle.dumps(trained_model))
    return p
