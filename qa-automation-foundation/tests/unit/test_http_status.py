import pytest

from src.utils.http_status import is_client_error, is_server_error, is_success

pytestmark = pytest.mark.unit


@pytest.mark.parametrize(
    "status, expected",
    [(200, True), (201, True), (299, True), (199, False), (300, False), (404, False)],
)
def test_is_success(status, expected):
    assert is_success(status) is expected


@pytest.mark.parametrize(
    "status, expected",
    [(400, True), (404, True), (499, True), (399, False), (500, False), (200, False)],
)
def test_is_client_error(status, expected):
    assert is_client_error(status) is expected


@pytest.mark.parametrize(
    "status, expected",
    [(500, True), (503, True), (599, True), (499, False), (600, False)],
)
def test_is_server_error(status, expected):
    assert is_server_error(status) is expected
