import allure
import pytest
from playwright.sync_api import Browser, Page

from api.cart_api import CartApi
from api.order_api import OrderApi
from api.product_api import ProductApi
from config.config import UI_URL, USER_EMAIL, USER_PASSWORD, ADMIN_EMAIL, ADMIN_PASSWORD
from helpers.auth_helper import AuthHelper
from helpers.test_data_helper import TestDataHelper
from pages.login_page import LoginPage


@pytest.fixture(scope="session")
def ui_test_product(admin_token):
    product_api = ProductApi()
    body = TestDataHelper.random_product_high_stock()
    response = product_api.create_product(admin_token, body)
    return response.json()


@pytest.fixture()
def page(browser: Browser, request):
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    yield page
    # Screenshot on failure
    if request.node.rep_call and request.node.rep_call.failed:
        screenshot = page.screenshot()
        allure.attach(screenshot, name="screenshot", attachment_type=allure.attachment_type.PNG)
    context.close()


@pytest.fixture()
def authenticated_page(browser: Browser, request):
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    # Login as user
    login_page = LoginPage(page)
    login_page.open_page()
    login_page.login(USER_EMAIL, USER_PASSWORD)
    page.wait_for_load_state("networkidle")
    yield page
    if request.node.rep_call and request.node.rep_call.failed:
        screenshot = page.screenshot()
        allure.attach(screenshot, name="screenshot", attachment_type=allure.attachment_type.PNG)
    context.close()


@pytest.fixture()
def admin_page(browser: Browser, request):
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    login_page = LoginPage(page)
    login_page.open_page()
    login_page.login(ADMIN_EMAIL, ADMIN_PASSWORD)
    page.wait_for_load_state("networkidle")
    yield page
    if request.node.rep_call and request.node.rep_call.failed:
        screenshot = page.screenshot()
        allure.attach(screenshot, name="screenshot", attachment_type=allure.attachment_type.PNG)
    context.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    import pytest
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
