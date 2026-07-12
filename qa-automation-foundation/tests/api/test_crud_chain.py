"""CRUD chain against the local fixture backend, not dummyjson.com.

Public mock APIs echo back a fake id on POST but never actually store the
record, so there's nothing honest to verify on a follow-up GET. The local
Flask fixture (tests/api/fixtures/fixture_server.py, started by the
crud_api_server fixture) gives us a real, disposable store instead — see
docs/STRATEGY.md for the full reasoning.

These tests are intentionally ordered (create -> read -> update -> delete)
and share state via the module-level `_state` dict, same as any real CRUD
walkthrough would be. Pytest runs tests within a file top-to-bottom by
default, so this only works as long as nobody reorders them with a
randomizer plugin — worth calling out for anyone touching this file.
"""

import pytest

from src.utils.test_data import unique_name
from tests.api.schemas.crud_resource_schema import Resource

pytestmark = pytest.mark.api

_state: dict = {}


def test_create_a_resource(http, crud_url):
    new_resource = {"name": unique_name("Katherine Johnson"), "job": "NASA Mathematician"}
    response = http.post(crud_url("/users"), json=new_resource)

    assert response.status_code == 201
    body = Resource.model_validate(response.json())
    assert body.name == new_resource["name"]

    _state["resource"] = new_resource
    _state["id"] = body.id


def test_the_created_resource_shows_up_when_fetched_by_id(http, crud_url):
    response = http.get(crud_url(f"/users/{_state['id']}"))

    assert response.status_code == 200
    body = response.json()
    assert body["name"] == _state["resource"]["name"]
    assert body["job"] == _state["resource"]["job"]


def test_the_created_resource_shows_up_in_the_full_list(http, crud_url):
    response = http.get(crud_url("/users"))
    users = response.json()

    found = next((u for u in users if u["id"] == _state["id"]), None)
    assert found is not None, f"expected to find resource id {_state['id']} in the list"
    assert found["name"] == _state["resource"]["name"]


def test_update_the_resource_and_confirm_it_persists(http, crud_url):
    response = http.patch(crud_url(f"/users/{_state['id']}"), json={"job": "Senior NASA Mathematician"})
    assert response.status_code == 200

    refetched = http.get(crud_url(f"/users/{_state['id']}")).json()
    assert refetched["job"] == "Senior NASA Mathematician"


def test_delete_the_resource_and_confirm_it_is_gone(http, crud_url):
    delete_response = http.delete(crud_url(f"/users/{_state['id']}"))
    assert delete_response.status_code == 200

    get_after_delete = http.get(crud_url(f"/users/{_state['id']}"))
    assert get_after_delete.status_code == 404
