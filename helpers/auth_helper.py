from api.auth_api import AuthApi
from config.config import ADMIN_EMAIL, ADMIN_PASSWORD, USER_EMAIL, USER_PASSWORD
from helpers.test_data_helper import TestDataHelper


class AuthHelper:
    _auth_api = AuthApi()

    @staticmethod
    def get_admin_token() -> str:
        response = AuthHelper._auth_api.login(ADMIN_EMAIL, ADMIN_PASSWORD)
        return response.json()["access_token"]

    @staticmethod
    def get_user_token() -> str:
        response = AuthHelper._auth_api.login(USER_EMAIL, USER_PASSWORD)
        return response.json()["access_token"]

    @staticmethod
    def register_and_get_token() -> str:
        auth_api = AuthApi()
        email = TestDataHelper.random_email()
        password = TestDataHelper.random_password()
        name = TestDataHelper.random_name()
        auth_api.register(email, password, name)
        response = auth_api.login(email, password)
        return response.json()["access_token"]
