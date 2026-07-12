"""GET /users — schema, status codes and response-time budget."""

import time

import pytest

from tests.api.schemas.user_schema import User, UsersList

pytestmark = pytest.mark.api


def test_list_matches_the_expected_schema(http, api_url):
    response = http.get(api_url("/users?limit=10"))

    assert response.status_code == 200

    body = UsersList.model_validate(response.json())
    assert 0 < len(body.users) <= 10


def test_every_user_matches_the_single_user_schema(http, api_url):
    response = http.get(api_url("/users?limit=5"))
    body = response.json()

    for raw_user in body["users"]:
        User.model_validate(raw_user)  # raises if the shape is wrong


def test_responds_within_the_configured_time_budget(http, api_url, config):
    start = time.monotonic()
    response = http.get(api_url("/users?limit=10"))
    elapsed = time.monotonic() - start

    assert response.status_code == 200
    assert elapsed < config.api_timeout_s


def test_a_known_user_resolves_with_200_and_the_right_id(http, api_url):
    response = http.get(api_url("/users/1"))

    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_a_non_existent_user_resolves_with_404(http, api_url):
    response = http.get(api_url("/users/999999"))
    assert response.status_code == 404
