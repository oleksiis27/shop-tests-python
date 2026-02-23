import allure
import pytest

from helpers.test_data_helper import TestDataHelper


@allure.epic("Shop API")
@allure.feature("Authentication")
class TestAuth:

    @allure.story("Registration")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("Register a new user with random data")
    def test_register_new_user(self, auth_api):
        email = TestDataHelper.random_email()
        password = TestDataHelper.random_password()
        name = TestDataHelper.random_name()

        response = auth_api.register(email, password, name)

        assert response.status_code == 201
        body = response.json()
        assert body["id"] is not None
        assert body["email"] is not None
        assert body["name"] is not None
        assert body["role"] is not None
        assert body["created_at"] is not None

    @allure.story("Registration")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Registering with duplicate email returns conflict")
    def test_register_duplicate_email(self, auth_api):
        email = TestDataHelper.random_email()
        password = TestDataHelper.random_password()
        name = TestDataHelper.random_name()

        response1 = auth_api.register(email, password, name)
        assert response1.status_code == 201

        response2 = auth_api.register(email, password, name)
        assert response2.status_code == 409

    @allure.story("Login")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("Login with valid admin credentials")
    def test_login_with_valid_credentials(self, auth_api):
        from config.config import ADMIN_EMAIL, ADMIN_PASSWORD
        response = auth_api.login(ADMIN_EMAIL, ADMIN_PASSWORD)

        assert response.status_code == 200
        body = response.json()
        assert body["access_token"]
        assert body["token_type"] == "bearer"

    @allure.story("Login")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Login with wrong password is rejected")
    def test_login_with_wrong_password(self, auth_api):
        from config.config import ADMIN_EMAIL
        response = auth_api.login(ADMIN_EMAIL, "wrongpassword")

        assert response.status_code == 401

    @allure.story("User Profile")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Get current user with valid token")
    def test_get_me_with_valid_token(self, auth_api, admin_token):
        response = auth_api.get_me(admin_token)

        assert response.status_code == 200
        body = response.json()
        assert body["id"] is not None
        assert body["email"] is not None
        assert body["role"] is not None

    @allure.story("User Profile")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Reject request without token")
    def test_get_me_without_token(self, auth_api):
        response = auth_api.get_me_without_token()

        assert response.status_code == 403

    @allure.story("User Profile")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Reject request with invalid token")
    def test_get_me_with_invalid_token(self, auth_api):
        response = auth_api.get_me_with_invalid_token()

        assert response.status_code == 401
