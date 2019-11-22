import pytest

from tests import utils


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
    with utils.tmp_dir() as directory:
        yield directory
