import pytest
from playwright.sync_api import Page

from tests.e2e.pages.inputs_page import InputsPage
from tests.e2e.pages.login_page import LoginPage

pytestmark = pytest.mark.e2e

# Data-driven negative cases for the login form. Parametrized so adding a
# new bad-input case later is a one-line addition, not a new test function.
LOGIN_VALIDATION_CASES = [
    pytest.param("", "SuperSecretPassword!", "Your username is invalid", id="empty_username"),
    pytest.param("tomsmith", "", "Your password is invalid", id="empty_password"),
    pytest.param("", "", "Your username is invalid", id="both_empty"),
    pytest.param("nope", "nope", "Your username is invalid", id="wrong_username_and_password"),
]


@pytest.mark.parametrize("username, password, expected", LOGIN_VALIDATION_CASES)
def test_login_form_rejects_bad_input(page: Page, username, password, expected):
    login = LoginPage(page)
    login.goto()
    login.login(username, password)
    login.expect_error(expected)


# Boundary testing on the numeric input field: the field only accepts
# digits (and a leading minus sign), so anything else should never end up
# in the DOM value — enforced by the browser, not our test, but exactly the
# kind of boundary/negative check worth automating.
NUMBER_INPUT_CASES = [
    pytest.param("123", "123", id="plain_integer"),
    pytest.param("-42", "-42", id="negative_integer"),
    pytest.param("3.14", "3.14", id="decimal"),
    pytest.param("abc", "", id="letters_are_rejected"),
    pytest.param("1e10", "1e10", id="exponent_notation_is_accepted_by_the_browser"),
    pytest.param("!!!", "", id="symbols_are_rejected"),
]


@pytest.mark.parametrize("value, expected", NUMBER_INPUT_CASES)
def test_number_field_boundary_values(page: Page, value, expected):
    inputs = InputsPage(page)
    inputs.goto()
    inputs.type(value)
    assert inputs.get_value() == expected
