"""POST /auth/login against dummyjson.com."""

import pytest

from tests.api.schemas.auth_schema import LoginSuccess, LoginError

pytestmark = pytest.mark.api

# dummyjson.com ships a handful of seeded accounts for exactly this purpose,
# see https://dummyjson.com/users for the full list.
VALID_USER = {"username": "emilys", "password": "emilyspass"}


def test_successful_login_returns_a_token(http, api_url):
    response = http.post(api_url("/auth/login"), json=VALID_USER)

    assert response.status_code == 200

    body = LoginSuccess.model_validate(response.json())
    assert body.username == VALID_USER["username"]
    assert len(body.accessToken) > 0


def test_login_with_wrong_password_is_rejected(http, api_url):
    response = http.post(
        api_url("/auth/login"),
        json={"username": VALID_USER["username"], "password": "definitely-not-the-password"},
    )

    assert response.status_code == 400

    body = LoginError.model_validate(response.json())
    assert "invalid credentials" in body.message.lower()


def test_login_with_unknown_username_is_rejected(http, api_url):
    response = http.post(
        api_url("/auth/login"),
        json={"username": "not-a-real-user-xyz", "password": "whatever"},
    )

    assert response.status_code == 400


def test_login_with_missing_password_is_rejected(http, api_url):
    response = http.post(api_url("/auth/login"), json={"username": VALID_USER["username"]})

    assert response.status_code in (400, 401)
