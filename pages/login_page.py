import allure
from playwright.sync_api import Page, expect
from config.config import UI_URL
from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.email_input = page.locator("input[name='email']")
        self.password_input = page.locator("input[name='password']")
        self.login_button = page.locator("button[type='submit']")
        self.register_link = page.locator("form a[href='/register']")
        self.error_message = page.locator("p.text-red-600")
        self.heading = page.locator("h1")

    @allure.step("Open login page")
    def open_page(self):
        self.open(f"{UI_URL}/login")

    @allure.step("Login with email: {email}")
    def login(self, email: str, password: str):
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.login_button.click()
        self.page.wait_for_load_state("networkidle")

    @allure.step("Click register link")
    def click_register_link(self):
        self.register_link.click()
        self.page.wait_for_load_state("networkidle")

    def should_have_heading(self, text: str):
        expect(self.heading).to_contain_text(text)

    def should_show_error(self):
        expect(self.error_message).to_be_visible()
