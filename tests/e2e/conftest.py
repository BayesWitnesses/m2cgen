import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--xx", dest='fail_fast_e2e', action="store_const", default=False, const=True,
        help="Fails e2e test immediately"
    )


@pytest.fixture
def xx(request):
    return request.config.getoption("--xx")
