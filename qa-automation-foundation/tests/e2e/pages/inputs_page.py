from playwright.sync_api import Page


class InputsPage:
    def __init__(self, page: Page):
        self.page = page
        self.number_input = page.locator('input[type="number"]')

    def goto(self):
        self.page.goto("/inputs")

    def type(self, value: str):
        self.number_input.fill("")
        self.number_input.type(value)

    def get_value(self) -> str:
        return self.number_input.input_value()
