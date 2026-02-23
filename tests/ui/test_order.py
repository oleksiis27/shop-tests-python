import allure
import pytest

from api.cart_api import CartApi
from api.order_api import OrderApi
from config.config import USER_EMAIL, USER_PASSWORD
from helpers.auth_helper import AuthHelper
from pages.orders_page import OrdersPage
from pages.login_page import LoginPage
from pages.components.nav_bar import NavBar


@allure.epic("Shop UI")
@allure.feature("Orders")
class TestOrderUi:

    @pytest.fixture(autouse=True)
    def setup(self, page, ui_test_product):
        # Create order via API for default user
        token = AuthHelper.get_user_token()
        cart_api = CartApi()
        order_api = OrderApi()
        cart_api.clear_cart(token)
        cart_api.add_item(token, ui_test_product["id"], 1)
        order_api.create_order(token)

        # Login in browser
        login_page = LoginPage(page)
        login_page.open_page()
        login_page.login(USER_EMAIL, USER_PASSWORD)

        # Navigate to orders via navbar (client-side routing)
        nav_bar = NavBar(page)
        nav_bar.should_be_logged_in()
        nav_bar.click_orders()

        self.page = page

    @allure.story("Order List")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("Created order visible in orders list")
    def test_order_appears_in_list(self):
        orders_page = OrdersPage(self.page)

        assert orders_page.get_orders_count() > 0
        assert "pending" in orders_page.get_order_status(0).lower()

    @allure.story("Order Details")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Order shows total amount")
    def test_order_details_show_total(self):
        orders_page = OrdersPage(self.page)

        total = orders_page.get_order_total(0)
        assert total
