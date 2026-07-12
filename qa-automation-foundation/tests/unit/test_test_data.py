import re

import pytest

from src.utils.test_data import random_email, unique_name

pytestmark = pytest.mark.unit


def test_unique_name_keeps_the_base_string_as_a_prefix():
    assert unique_name("Katherine Johnson").startswith("Katherine Johnson ")


def test_unique_name_is_different_on_every_call():
    names = {unique_name("Same Base") for _ in range(20)}
    assert len(names) == 20


def test_random_email_looks_like_an_email_address():
    assert re.match(r"^[\w.]+@example\.test$", random_email())


def test_random_email_respects_a_custom_prefix():
    assert random_email("crud").startswith("crud.")


def test_random_email_is_unique_across_calls():
    emails = {random_email() for _ in range(20)}
    assert len(emails) == 20
