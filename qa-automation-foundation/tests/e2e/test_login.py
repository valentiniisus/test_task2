import re

import pytest
from playwright.sync_api import Page, expect

from tests.e2e.pages.login_page import LoginPage

pytestmark = pytest.mark.e2e


def test_successful_login_lands_on_the_secure_area(page: Page, config):
    login = LoginPage(page)
    login.goto()
    login.login(config.ui_login, config.ui_password)
    login.expect_logged_in()


def test_logging_out_returns_to_the_login_page(page: Page, config):
    login = LoginPage(page)
    login.goto()
    login.login(config.ui_login, config.ui_password)
    login.expect_logged_in()

    page.locator('a[href="/logout"]').click()
    expect(page).to_have_url(re.compile(r"/login$"))
    expect(login.flash_message).to_contain_text("You logged out of the secure area")


def test_wrong_password_is_rejected(page: Page, config):
    login = LoginPage(page)
    login.goto()
    login.login(config.ui_login, "not-the-real-password")
    login.expect_error("Your password is invalid")


def test_unknown_username_is_rejected(page: Page):
    login = LoginPage(page)
    login.goto()
    login.login("not-a-real-user", "whatever123")
    login.expect_error("Your username is invalid")
