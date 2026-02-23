import allure
from playwright.sync_api import Page, expect
from config.config import UI_URL
from pages.base_page import BasePage


class AdminPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.heading = page.locator("h1")
        self.orders_tab = page.get_by_role("button", name="Orders")
        self.products_tab = page.get_by_role("button", name="Products")
        self.order_cards = page.locator("div.bg-white.p-6.rounded-lg.shadow")
        self.add_product_button = page.get_by_role("button", name="Add Product")
        self.product_rows = page.locator("table tbody tr")
        # Product form
        self.name_input = page.locator("form input[name='name']")
        self.price_input = page.locator("form input[name='price']")
        self.stock_input = page.locator("form input[name='stock']")
        self.category_select = page.locator("form select[name='category_id']")
        self.description_input = page.locator("form textarea[name='description']")
        self.image_url_input = page.locator("form input[name='image_url']")
        self.create_button = page.get_by_role("button", name="Create")

    @allure.step("Open admin page")
    def open_page(self):
        self.open(f"{UI_URL}/admin")

    @allure.step("Click Orders tab")
    def click_orders_tab(self):
        self.orders_tab.click()
        self.page.wait_for_load_state("networkidle")

    @allure.step("Click Products tab")
    def click_products_tab(self):
        self.products_tab.click()
        self.page.wait_for_load_state("networkidle")

    @allure.step("Click Add Product")
    def click_add_product(self):
        self.add_product_button.click()

    @allure.step("Fill product form and create")
    def add_product(self, name: str, description: str, price: float, stock: int,
                    category: str, image_url: str):
        self.name_input.fill(name)
        self.price_input.fill(str(price))
        self.stock_input.fill(str(stock))
        self.category_select.select_option(label=category)
        self.description_input.fill(description)
        self.image_url_input.fill(image_url)
        self.create_button.click()
        self.page.wait_for_load_state("networkidle")

    @allure.step("Update pending order status to confirmed")
    def update_pending_order_to_confirmed(self):
        # Find the first order with a "confirmed" button (i.e., a pending order)
        confirmed_button = self.page.get_by_role("button", name="confirmed").first
        confirmed_button.click()
        self.page.wait_for_load_state("networkidle")

    @allure.step("Delete last product")
    def delete_last_product(self):
        self.page.on("dialog", lambda dialog: dialog.accept())
        last_row = self.product_rows.last
        last_row.get_by_role("button", name="Delete").click()
        self.page.wait_for_load_state("networkidle")

    def get_order_cards_count(self) -> int:
        return self.order_cards.count()

    def get_product_rows_count(self) -> int:
        return self.product_rows.count()

    def get_first_order_status(self) -> str:
        return self.order_cards.first.locator("span.rounded-full").inner_text()

    def should_have_heading(self, text: str):
        expect(self.heading).to_contain_text(text)
