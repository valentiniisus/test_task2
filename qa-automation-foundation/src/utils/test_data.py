"""Helpers for keeping test data unique across parallel runs, so tests
don't collide on a shared fixture/backend."""

from __future__ import annotations

import random
import time


def unique_name(base: str) -> str:
    suffix = f"{int(time.time() * 1000)}-{random.randint(0, 9999)}"
    return f"{base} {suffix}"


def random_email(prefix: str = "qa") -> str:
    suffix = f"{int(time.time() * 1000)}{random.randint(0, 9999)}"
    return f"{prefix}.{suffix}@example.test"
