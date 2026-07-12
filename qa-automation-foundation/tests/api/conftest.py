import pytest
import requests


@pytest.fixture(scope="session")
def api_url(config):
    """Builds full dummyjson.com URLs from a relative path, e.g. api_url('/users')."""

    def _build(path: str) -> str:
        return f"{config.api_base_url}{path}"

    return _build


@pytest.fixture(scope="session")
def http():
    return requests.Session()


@pytest.fixture
def crud_url(crud_api_server):
    """Builds full URLs against the local Flask fixture backend. Depending on
    crud_api_server guarantees the server is up before any test in this
    fixture's chain runs."""

    def _build(path: str) -> str:
        return f"{crud_api_server}{path}"

    return _build
