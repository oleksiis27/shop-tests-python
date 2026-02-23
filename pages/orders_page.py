import allure
from playwright.sync_api import Page, expect
from config.config import UI_URL
from pages.base_page import BasePage


class OrdersPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.orders = page.locator("div.bg-white.p-6.rounded-lg.shadow")
        self.heading = page.locator("h1")

    @allure.step("Open orders page")
    def open_page(self):
        self.open(f"{UI_URL}/orders")

    def get_orders_count(self) -> int:
        self.orders.first.wait_for(state="visible", timeout=10000)
        return self.orders.count()

    def get_order_status(self, index: int = 0) -> str:
        return self.orders.nth(index).locator("span.rounded-full").inner_text()

    def get_order_total(self, index: int = 0) -> str:
        return self.orders.nth(index).locator("p.text-lg.font-bold").inner_text()
