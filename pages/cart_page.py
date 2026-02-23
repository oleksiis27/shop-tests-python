import allure
from playwright.sync_api import Page, expect
from config.config import UI_URL
from pages.base_page import BasePage


class CartPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.heading = page.locator("h1")
        self.cart_items = page.locator("div.bg-white.p-4.rounded-lg")
        self.total_price = page.locator("p.text-2xl.font-bold")
        self.checkout_button = page.get_by_role("button", name="Checkout")
        self.clear_cart_button = page.get_by_role("button", name="Clear Cart")
        self.empty_cart_message = page.get_by_text("Your cart is empty.")

    @allure.step("Open cart page")
    def open_page(self):
        self.open(f"{UI_URL}/cart")

    @allure.step("Click increase quantity for item {index}")
    def increase_quantity(self, index: int = 0):
        initial_total = self.total_price.inner_text()
        item = self.cart_items.nth(index)
        item.get_by_role("button", name="+").click()
        self.page.wait_for_load_state("networkidle")
        # Wait for total to actually change
        expect(self.total_price).not_to_have_text(initial_total, timeout=10000)

    @allure.step("Click decrease quantity for item {index}")
    def decrease_quantity(self, index: int = 0):
        item = self.cart_items.nth(index)
        item.get_by_role("button", name="-").click()
        self.page.wait_for_load_state("networkidle")

    @allure.step("Remove item {index}")
    def remove_item(self, index: int = 0):
        item = self.cart_items.nth(index)
        item.get_by_role("button", name="Remove").click()
        self.page.wait_for_load_state("networkidle")

    @allure.step("Click Clear Cart")
    def click_clear_cart(self):
        self.clear_cart_button.click()
        self.page.wait_for_load_state("networkidle")

    @allure.step("Click Checkout")
    def click_checkout(self):
        self.checkout_button.click()
        self.page.wait_for_url("**/orders", timeout=10000)

    def get_total_text(self) -> str:
        return self.total_price.inner_text()

    def get_items_count(self) -> int:
        return self.cart_items.count()

    def should_be_empty(self):
        expect(self.empty_cart_message).to_be_visible()

    def should_have_heading(self, text: str):
        expect(self.heading).to_contain_text(text)
