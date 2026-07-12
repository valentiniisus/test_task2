"""pytest-playwright picks up the `base_url` fixture automatically and uses
it for every page.goto("/relative/path") call, so specs don't hardcode the
host."""

import pytest

from config.env import get_config


@pytest.fixture(scope="session")
def base_url():
    return get_config().ui_base_url


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    cfg = get_config()
    return {
        **browser_context_args,
        "base_url": cfg.ui_base_url,
    }
