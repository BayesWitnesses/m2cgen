import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--fast", action="store_const",
        default=False, const=True, help="Run e2e tests fast"
    )


@pytest.fixture
def is_fast(request):
    return request.config.getoption("--fast")
