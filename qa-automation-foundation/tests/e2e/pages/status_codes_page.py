from playwright.sync_api import Locator, Page


class StatusCodesPage:
    def __init__(self, page: Page):
        self.page = page

    def goto(self):
        self.page.goto("/status_codes")

    def link_for(self, code: int) -> Locator:
        # the-internet renders these as relative hrefs (status_codes/200, no
        # leading slash), so match on the suffix rather than the full path.
        return self.page.locator(f'a[href$="status_codes/{code}"]')

    def message_locator(self) -> Locator:
        return self.page.locator(".example p")
