import pytest

from helpers.auth_helper import AuthHelper
from helpers.test_data_helper import TestDataHelper


@pytest.fixture(scope="session")
def user_token():
    return AuthHelper.get_user_token()


@pytest.fixture(scope="session")
def test_product(admin_token, product_api):
    body = TestDataHelper.random_product_high_stock()
    response = product_api.create_product(admin_token, body)
    return response.json()


@pytest.fixture(scope="session")
def test_product_2(admin_token, product_api):
    body = TestDataHelper.random_product_high_stock()
    response = product_api.create_product(admin_token, body)
    return response.json()
