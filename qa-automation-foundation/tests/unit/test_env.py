import pytest

from config.env import get_config

pytestmark = pytest.mark.unit


def test_defaults_to_dev_when_no_override(monkeypatch):
    monkeypatch.delenv("TEST_ENV", raising=False)
    get_config.cache_clear()
    cfg = get_config()
    assert cfg.env == "dev"


def test_loads_staging_via_explicit_override():
    cfg = get_config(env_override="staging")
    assert cfg.env == "staging"
    assert cfg.api_timeout_ms == 8000


def test_loads_prod_via_explicit_override():
    cfg = get_config(env_override="prod")
    assert cfg.env == "prod"
    assert cfg.api_timeout_ms == 10000


@pytest.mark.parametrize("env_name", ["dev", "staging", "prod"])
def test_every_environment_resolves_the_required_fields(env_name):
    cfg = get_config(env_override=env_name)
    assert cfg.api_base_url
    assert cfg.ui_base_url
    assert cfg.crud_api_base_url


def test_rejects_an_unknown_environment_name():
    with pytest.raises(ValueError, match="Unknown TEST_ENV"):
        get_config(env_override="nonexistent")
