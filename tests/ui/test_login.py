import allure
import pytest

from config.config import USER_EMAIL, USER_PASSWORD
from pages.login_page import LoginPage
from pages.components.nav_bar import NavBar


@allure.epic("Shop UI")
@allure.feature("Login")
class TestLogin:

    @allure.story("Valid Login")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("Login with valid credentials redirects and shows logged-in state")
    def test_login_with_valid_credentials(self, page):
        login_page = LoginPage(page)
        nav_bar = NavBar(page)

        login_page.open_page()
        login_page.login(USER_EMAIL, USER_PASSWORD)

        nav_bar.should_be_logged_in()

    @allure.story("Invalid Login")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Wrong password shows error message")
    def test_login_with_wrong_password(self, page):
        login_page = LoginPage(page)

        login_page.open_page()
        login_page.login(USER_EMAIL, "wrongpassword")

        login_page.should_show_error()

    @allure.story("Navigation")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Click register link navigates to register page")
    def test_navigate_to_register_page(self, page):
        login_page = LoginPage(page)

        login_page.open_page()
        login_page.click_register_link()

        assert "/register" in page.url

    @allure.story("Logout")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Logout shows login and register links")
    def test_logout_shows_login_register_links(self, page):
        login_page = LoginPage(page)
        nav_bar = NavBar(page)

        login_page.open_page()
        login_page.login(USER_EMAIL, USER_PASSWORD)
        nav_bar.should_be_logged_in()

        nav_bar.click_logout()

        nav_bar.login_link_should_be_visible()
        nav_bar.register_link_should_be_visible()
