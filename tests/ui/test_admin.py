import allure
import pytest

from api.cart_api import CartApi
from api.order_api import OrderApi
from config.config import ADMIN_EMAIL, ADMIN_PASSWORD
from helpers.auth_helper import AuthHelper
from pages.admin_page import AdminPage
from pages.login_page import LoginPage


@allure.epic("Shop UI")
@allure.feature("Admin Panel")
class TestAdmin:

    @pytest.fixture(autouse=True)
    def setup(self, admin_page, ui_test_product):
        # Ensure there's at least one pending order
        token = AuthHelper.register_and_get_token()
        cart_api = CartApi()
        order_api = OrderApi()
        cart_api.add_item(token, ui_test_product["id"], 1)
        order_api.create_order(token)

        self.page = admin_page

    @allure.story("Admin Orders")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("Admin can view all orders")
    def test_admin_sees_all_orders(self):
        admin = AdminPage(self.page)
        admin.open_page()
        admin.click_orders_tab()

        assert admin.get_order_cards_count() > 0

    @allure.story("Admin Orders")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Admin changes order status to confirmed")
    def test_admin_updates_order_status(self):
        admin = AdminPage(self.page)
        admin.open_page()
        admin.click_orders_tab()
        admin.update_pending_order_to_confirmed()

        # Verify at least one order shows confirmed status
        statuses = self.page.locator("span.rounded-full")
        status_texts = [statuses.nth(i).inner_text() for i in range(statuses.count())]
        assert any("confirmed" in s.lower() for s in status_texts)

    @allure.story("Admin Products")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Admin creates new product")
    def test_admin_creates_product(self):
        admin = AdminPage(self.page)
        admin.open_page()
        admin.click_products_tab()
        self.page.wait_for_load_state("networkidle")

        initial_count = admin.get_product_rows_count()
        admin.click_add_product()
        admin.add_product(
            "Test Product UI",
            "Test description",
            29.99,
            50,
            "Electronics",
            "https://example.com/test.jpg",
        )
        self.page.wait_for_timeout(1000)

        assert admin.get_product_rows_count() > initial_count

    @allure.story("Admin Products")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Admin deletes product")
    def test_admin_deletes_product(self):
        admin = AdminPage(self.page)
        admin.open_page()
        admin.click_products_tab()
        self.page.wait_for_load_state("networkidle")

        initial_count = admin.get_product_rows_count()
        admin.delete_last_product()
        self.page.wait_for_timeout(1000)

        assert admin.get_product_rows_count() < initial_count
