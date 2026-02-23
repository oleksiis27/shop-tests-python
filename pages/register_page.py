import allure
from playwright.sync_api import Page, expect
from config.config import UI_URL
from pages.base_page import BasePage


class RegisterPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.name_input = page.locator("input[name='name']")
        self.email_input = page.locator("input[name='email']")
        self.password_input = page.locator("input[name='password']")
        self.register_button = page.locator("button[type='submit']")
        self.login_link = page.locator("form a[href='/login']")
        self.error_message = page.locator("p.text-red-600")
        self.heading = page.locator("h1")

    @allure.step("Open register page")
    def open_page(self):
        self.open(f"{UI_URL}/register")

    @allure.step("Register with name: {name}, email: {email}")
    def register(self, name: str, email: str, password: str):
        self.name_input.fill(name)
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.register_button.click()
        self.page.wait_for_load_state("networkidle")

    @allure.step("Click login link")
    def click_login_link(self):
        self.login_link.click()
        self.page.wait_for_load_state("networkidle")

    def should_have_heading(self, text: str):
        expect(self.heading).to_contain_text(text)

    def should_show_error(self):
        expect(self.error_message).to_be_visible()
