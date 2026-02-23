import allure
import pytest
from playwright.sync_api import sync_playwright

from api.auth_api import AuthApi
from api.product_api import ProductApi
from api.cart_api import CartApi
from api.order_api import OrderApi
from helpers.auth_helper import AuthHelper
from helpers.test_data_helper import TestDataHelper


@pytest.fixture(scope="session")
def auth_api():
    return AuthApi()


@pytest.fixture(scope="session")
def product_api():
    return ProductApi()


@pytest.fixture(scope="session")
def cart_api():
    return CartApi()


@pytest.fixture(scope="session")
def order_api():
    return OrderApi()


@pytest.fixture(scope="session")
def admin_token():
    return AuthHelper.get_admin_token()


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()
