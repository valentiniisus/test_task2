"""Environment config loader.

Reads config/environments/<TEST_ENV>.env and exposes it as a typed object.
TEST_ENV defaults to "dev" if not set. This is the single place that knows
where env files live and what variables are required — tests never read
os.environ directly.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from functools import lru_cache

from dotenv import dotenv_values

VALID_ENVS = ("dev", "staging", "prod")

REPO_ROOT = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class TestConfig:
    env: str
    api_base_url: str
    crud_api_base_url: str
    ui_base_url: str
    ui_login: str
    ui_password: str
    api_timeout_ms: int
    ui_timeout_ms: int

    @property
    def api_timeout_s(self) -> float:
        return self.api_timeout_ms / 1000

    @property
    def ui_timeout_ms_float(self) -> float:
        return float(self.ui_timeout_ms)


def _resolve_env_name() -> str:
    raw = os.environ.get("TEST_ENV", "dev").lower()
    if raw not in VALID_ENVS:
        raise ValueError(f'Unknown TEST_ENV "{raw}". Use one of: {", ".join(VALID_ENVS)}.')
    return raw


def _require(values: dict, key: str) -> str:
    value = values.get(key) or os.environ.get(key)
    if not value:
        raise ValueError(f'Missing required env var "{key}". Check config/environments/*.env')
    return value


@lru_cache(maxsize=None)
def get_config(env_override: str | None = None) -> TestConfig:
    """Load config for the current TEST_ENV. Cached per env name so repeated
    calls within a test run don't re-read the file every time. Pass
    env_override explicitly (e.g. in tests) to bypass TEST_ENV."""
    env_name = env_override or _resolve_env_name()
    if env_name not in VALID_ENVS:
        raise ValueError(f'Unknown TEST_ENV "{env_name}". Use one of: {", ".join(VALID_ENVS)}.')

    env_file = REPO_ROOT / "config" / "environments" / f"{env_name}.env"
    if not env_file.exists():
        raise FileNotFoundError(f"Env file not found: {env_file}")

    values = dotenv_values(env_file)

    return TestConfig(
        env=env_name,
        api_base_url=_require(values, "API_BASE_URL"),
        crud_api_base_url=_require(values, "CRUD_API_BASE_URL"),
        ui_base_url=_require(values, "UI_BASE_URL"),
        ui_login=_require(values, "UI_LOGIN"),
        ui_password=_require(values, "UI_PASSWORD"),
        api_timeout_ms=int(values.get("API_TIMEOUT_MS", 5000)),
        ui_timeout_ms=int(values.get("UI_TIMEOUT_MS", 15000)),
    )
