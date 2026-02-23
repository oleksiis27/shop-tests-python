import allure
from playwright.sync_api import Page, expect
from config.config import UI_URL
from pages.base_page import BasePage


class ProductPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.product_name = page.locator("h1")
        self.price = page.locator("p.text-3xl.font-bold")
        self.description = page.locator("p.text-gray-600")
        self.quantity_input = page.locator("input[type='number']")
        self.add_to_cart_button = page.get_by_role("button", name="Add to Cart")
        self.success_message = page.locator("p.text-green-600")

    @allure.step("Open product page: {product_id}")
    def open_page(self, product_id: int):
        self.open(f"{UI_URL}/products/{product_id}")

    @allure.step("Set quantity to {quantity}")
    def set_quantity(self, quantity: int):
        self.quantity_input.fill(str(quantity))

    @allure.step("Click Add to Cart")
    def click_add_to_cart(self):
        self.add_to_cart_button.click()

    def should_show_success_message(self):
        expect(self.success_message).to_be_visible(timeout=10000)

    def should_have_product_details(self):
        expect(self.product_name).to_be_visible()
        expect(self.price).to_be_visible()
