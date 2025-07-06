from playwright.sync_api import Page, expect
from tests.constants.endpoints import BASE_UI_URL
from tests.constants.timeouts import Timeout


class BasePage:

    def __init__(self, page: Page):
        self.page = page
        self.base_url = BASE_UI_URL

    def open(self, path=""):
        self.page.goto(f"{self.base_url}{path}")

    def is_url(self, path: str):
        expected_url = f"{self.base_url}{path}"
        expect(self.page).to_have_url(expected_url, timeout=Timeout.FIVE_SECONDS.value)