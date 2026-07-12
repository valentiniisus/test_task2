import re

from playwright.sync_api import Page, expect


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.locator("#username")
        self.password_input = page.locator("#password")
        self.submit_button = page.locator('button[type="submit"]')
        self.flash_message = page.locator("#flash")

    def goto(self):
        self.page.goto("/login")

    def login(self, username: str, password: str):
        # fill() clears first, so this is safe to call more than once per test
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.submit_button.click()

    def expect_logged_in(self):
        expect(self.page).to_have_url(re.compile(r"/secure$"))
        expect(self.flash_message).to_contain_text("You logged into a secure area")

    def expect_error(self, text: str):
        expect(self.flash_message).to_contain_text(text)
        expect(self.page).to_have_url(re.compile(r"/login$"))
