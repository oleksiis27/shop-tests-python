import allure
import pytest

from config.config import ADMIN_EMAIL
from helpers.test_data_helper import TestDataHelper
from pages.register_page import RegisterPage
from pages.components.nav_bar import NavBar


@allure.epic("Shop UI")
@allure.feature("Registration")
class TestRegister:

    @allure.story("Valid Registration")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("Register new user auto-logs in")
    def test_register_new_user(self, page):
        register_page = RegisterPage(page)
        nav_bar = NavBar(page)

        register_page.open_page()
        register_page.register(
            TestDataHelper.random_name(),
            TestDataHelper.random_email(),
            TestDataHelper.random_password(),
        )

        nav_bar.should_be_logged_in()

    @allure.story("Duplicate Registration")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Registering with existing email shows error")
    def test_register_with_existing_email(self, page):
        register_page = RegisterPage(page)

        register_page.open_page()
        register_page.register("Test User", ADMIN_EMAIL, "password123")

        register_page.should_show_error()

    @allure.story("Navigation")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Click login link navigates to login page")
    def test_navigate_to_login_page(self, page):
        register_page = RegisterPage(page)

        register_page.open_page()
        register_page.click_login_link()

        assert "/login" in page.url
