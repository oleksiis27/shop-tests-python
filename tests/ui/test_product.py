import allure
import pytest

from pages.product_page import ProductPage
from pages.login_page import LoginPage
from pages.components.nav_bar import NavBar
from config.config import USER_EMAIL, USER_PASSWORD


@allure.epic("Shop UI")
@allure.feature("Product Page")
class TestProduct:

    @allure.story("Product Details")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("Product page shows name and price")
    def test_product_page_shows_details(self, page, ui_test_product):
        product_page = ProductPage(page)

        product_page.open_page(ui_test_product["id"])

        product_page.should_have_product_details()

    @allure.story("Add to Cart")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Logged-in user can add product to cart")
    def test_add_product_to_cart(self, page, ui_test_product):
        # Login first
        login_page = LoginPage(page)
        login_page.open_page()
        login_page.login(USER_EMAIL, USER_PASSWORD)

        # Verify logged-in state before proceeding
        nav_bar = NavBar(page)
        nav_bar.should_be_logged_in()

        product_page = ProductPage(page)
        product_page.open_page(ui_test_product["id"])
        product_page.set_quantity(1)
        product_page.click_add_to_cart()

        product_page.should_show_success_message()

    @allure.story("Add to Cart")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Unauthorized user redirected to login")
    def test_unauthorized_add_to_cart_redirects_to_login(self, page, ui_test_product):
        product_page = ProductPage(page)

        product_page.open_page(ui_test_product["id"])
        product_page.click_add_to_cart()

        page.wait_for_url("**/login", timeout=10000)
        assert "/login" in page.url
