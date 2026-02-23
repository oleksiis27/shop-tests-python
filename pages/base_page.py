import allure
from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    @allure.step("Open URL: {url}")
    def open(self, url: str):
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")
        self.wait_for_react_ready()

    @allure.step("Wait for React to be ready")
    def wait_for_react_ready(self):
        self.page.wait_for_selector("nav", state="visible")
        self.page.wait_for_timeout(500)
