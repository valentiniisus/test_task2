"""Confirms the number the page displays actually matches the HTTP status
Playwright observed on the network, instead of just trusting the text on
screen says what we expect."""

import pytest
from playwright.sync_api import Page, expect

from tests.e2e.pages.status_codes_page import StatusCodesPage

pytestmark = pytest.mark.e2e

CODES_TO_CHECK = [200, 301, 404, 500]


@pytest.mark.parametrize("code", CODES_TO_CHECK)
def test_status_code_page_reflects_the_real_response(page: Page, code):
    status_codes = StatusCodesPage(page)
    status_codes.goto()

    with page.expect_response(lambda res: f"/status_codes/{code}" in res.url) as response_info:
        status_codes.link_for(code).click()

    response = response_info.value
    assert response.status == code
    expect(status_codes.message_locator()).to_contain_text(f"This page returned a {code} status code")
