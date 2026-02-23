import allure
from playwright.sync_api import Page, expect
from config.config import UI_URL
from pages.base_page import BasePage


class HomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.search_input = page.locator("input[name='search']")
        self.search_button = page.locator("form button[type='submit']")
        self.category_select = page.locator("select").first
        self.sort_select = page.locator("select").last
        self.product_cards = page.locator(".grid a")
        self.next_button = page.get_by_role("button", name="Next")
        self.previous_button = page.get_by_role("button", name="Previous")

    @allure.step("Open home page")
    def open_page(self):
        self.open(f"{UI_URL}/")

    @allure.step("Search for: {term}")
    def search(self, term: str):
        self.search_input.fill(term)
        self.search_button.click()
        self.page.wait_for_load_state("networkidle")

    @allure.step("Filter by category: {category}")
    def filter_by_category(self, category: str):
        self.category_select.select_option(label=category)
        self.page.wait_for_load_state("networkidle")

    @allure.step("Sort by: {sort_option}")
    def sort_by(self, sort_option: str):
        self.sort_select.select_option(value=sort_option)
        self.page.wait_for_load_state("networkidle")

    @allure.step("Click next page")
    def click_next_page(self):
        self.next_button.click()
        self.page.wait_for_load_state("networkidle")

    def get_product_cards_count(self) -> int:
        return self.product_cards.count()
