import allure
import pytest

from api.cart_api import CartApi
from config.config import USER_EMAIL, USER_PASSWORD
from helpers.auth_helper import AuthHelper
from pages.cart_page import CartPage
from pages.product_page import ProductPage
from pages.login_page import LoginPage


@allure.epic("Shop UI")
@allure.feature("Cart")
class TestCartUi:

    @pytest.fixture(autouse=True)
    def setup(self, page, ui_test_product):
        # Login
        login_page = LoginPage(page)
        login_page.open_page()
        login_page.login(USER_EMAIL, USER_PASSWORD)

        # Add product to cart via API for speed
        token = AuthHelper.get_user_token()
        cart_api = CartApi()
        cart_api.clear_cart(token)
        cart_api.add_item(token, ui_test_product["id"], 1)

        self.page = page
        self.product_id = ui_test_product["id"]

    @allure.story("View Cart")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("Added product visible in cart")
    def test_added_product_visible_in_cart(self):
        cart_page = CartPage(self.page)
        cart_page.open_page()

        assert cart_page.get_items_count() > 0

    @allure.story("Update Quantity")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Increasing quantity updates total")
    def test_change_quantity_updates_total(self):
        cart_page = CartPage(self.page)
        cart_page.open_page()

        initial_total = cart_page.get_total_text()
        cart_page.increase_quantity(0)
        updated_total = cart_page.get_total_text()

        assert updated_total != initial_total

    @allure.story("Remove Item")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Remove item from cart")
    def test_remove_item_from_cart(self):
        cart_page = CartPage(self.page)
        cart_page.open_page()

        cart_page.remove_item(0)

        cart_page.should_be_empty()

    @allure.story("Clear Cart")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Clear all items from cart")
    def test_clear_cart_removes_all_items(self):
        cart_page = CartPage(self.page)
        cart_page.open_page()

        cart_page.click_clear_cart()

        cart_page.should_be_empty()

    @allure.story("Checkout")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("Checkout creates order and redirects to orders")
    def test_checkout_creates_order(self):
        cart_page = CartPage(self.page)
        cart_page.open_page()

        cart_page.click_checkout()

        assert "/orders" in self.page.url
