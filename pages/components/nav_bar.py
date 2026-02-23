import allure
from playwright.sync_api import Page, expect


class NavBar:
    def __init__(self, page: Page):
        self.page = page
        self.cart_link = page.locator("a[href='/cart']")
        self.orders_link = page.locator("a[href='/orders']")
        self.admin_link = page.locator("a[href='/admin']")
        self.login_link = page.locator("a[href='/login']")
        self.register_link = page.locator("a.bg-indigo-600")
        self.logout_button = page.locator("nav button")
        self.user_name = page.locator("nav span.text-sm")

    @allure.step("Click Cart")
    def click_cart(self):
        self.cart_link.click()
        self.page.wait_for_load_state("networkidle")

    @allure.step("Click Orders")
    def click_orders(self):
        self.orders_link.click()
        self.page.wait_for_load_state("networkidle")

    @allure.step("Click Admin")
    def click_admin(self):
        self.admin_link.click()
        self.page.wait_for_load_state("networkidle")

    @allure.step("Click Login")
    def click_login(self):
        self.login_link.click()
        self.page.wait_for_load_state("networkidle")

    @allure.step("Click Register")
    def click_register(self):
        self.register_link.click()
        self.page.wait_for_load_state("networkidle")

    @allure.step("Click Logout")
    def click_logout(self):
        self.logout_button.click()
        self.page.wait_for_load_state("networkidle")

    def get_user_name(self) -> str:
        return self.user_name.inner_text()

    def should_be_logged_in(self):
        expect(self.logout_button).to_be_visible()

    def login_link_should_be_visible(self):
        expect(self.login_link).to_be_visible()

    def register_link_should_be_visible(self):
        expect(self.register_link).to_be_visible()
