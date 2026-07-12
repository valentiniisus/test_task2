"""Root-level fixtures shared by API, E2E and unit tests."""

from __future__ import annotations

from urllib.parse import urlparse

import pytest

from config.env import get_config
from tests.api.fixtures.fixture_server import FixtureServerThread


@pytest.fixture(scope="session")
def config():
    return get_config()


@pytest.fixture(scope="session")
def crud_api_server(config):
    """Starts the local Flask fixture backend once per test session, for
    the CRUD-chain test only. Torn down automatically when the session
    ends — no state survives between runs.
    """
    port = urlparse(config.crud_api_base_url).port or 3001
    server = FixtureServerThread(port=port)
    server.start()
    yield config.crud_api_base_url
    server.stop()
    server.join(timeout=5)
