from playwright.sync_api import Page, expect, Locator

from tests.constants.timeouts import Timeout
from tests.ui.pages.base_page import BasePage


class PaymentPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.movie_title: Locator = page.locator("div:has(h3:text('Покупка билета')) >> p.text-muted-foreground")
        self.price: Locator = page.locator("div:has-text('Сумма к оплате') >> p.text-3xl")
        self.amount_input: Locator = page.locator('[data-qa-id="payment_amount_input"]')
        self.card_number_input: Locator = page.locator('[data-qa-id="payment_card_number_input"]')
        self.card_holder_input: Locator = page.locator('[data-qa-id="payment_card_holder_input"]')
        self.month_select: Locator = page.locator('[data-qa-id="payment_card_month_select"]')
        self.year_select: Locator = page.locator('[data-qa-id="payment_card_year_select"]')
        self.cvc_input: Locator = page.locator('[data-qa-id="payment_card_cvc_input"]')
        self.submit_button: Locator = page.locator('[data-qa-id="payment_submit_button"]')

    def open(self, movie_id: int):
        super().open(f"/payment?movieId={movie_id}")

    def fill_payment_details(self, card_number: str, card_holder: str, month: str, year: str, cvc: str, amount: int = 1):
        self.amount_input.fill(str(amount))
        self.card_number_input.fill(card_number)
        self.card_holder_input.fill(card_holder)
        
        self.month_select.click()
        self.page.get_by_role("option", name=month).click()
        
        self.year_select.click()
        self.page.get_by_role("option", name=year).click()
        
        self.cvc_input.fill(cvc)

    def submit_payment(self):
        self.submit_button.click()

    def check_movie_title_is_visible(self, title_part: str):
        expect(self.movie_title).to_contain_text(title_part)

    def check_price_is_visible(self):
        expect(self.price).to_be_visible()

    def check_submit_button_is_disabled(self):
        expect(self.submit_button).to_be_disabled()

    def check_validation_error_is_visible(self, message: str):
        error_locator = self.page.get_by_text(message)
        expect(error_locator).to_be_visible(timeout=Timeout.FIVE_SECONDS.value)