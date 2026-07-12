import re

import pytest
from playwright.sync_api import Page, expect

pytestmark = pytest.mark.e2e


def test_can_open_an_example_page_and_come_back(page: Page):
    page.goto("/")
    expect(page.locator("h2")).to_have_text("Available Examples")

    page.locator('a[href="/checkboxes"]').click()
    expect(page).to_have_url(re.compile(r"/checkboxes$"))
    expect(page.locator("h3")).to_have_text("Checkboxes")

    page.go_back()
    expect(page).to_have_url("https://the-internet.herokuapp.com/")
    expect(page.locator("h2")).to_have_text("Available Examples")


def test_can_move_between_two_unrelated_pages_via_the_homepage(page: Page):
    page.goto("/")
    page.locator('a[href="/dropdown"]').click()
    expect(page.locator("h3")).to_have_text("Dropdown List")

    page.goto("/")
    page.locator('a[href="/add_remove_elements/"]').click()
    expect(page.locator("h3")).to_have_text("Add/Remove Elements")
