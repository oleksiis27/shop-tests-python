import allure
import requests
from config.config import BASE_URL


class AuthApi:
    def __init__(self):
        self.base_url = f"{BASE_URL}/api/auth"

    @allure.step("Register user with email: {email}")
    def register(self, email: str, password: str, name: str) -> requests.Response:
        return requests.post(
            f"{self.base_url}/register",
            json={"email": email, "password": password, "name": name},
        )

    @allure.step("Login with email: {email}")
    def login(self, email: str, password: str) -> requests.Response:
        return requests.post(
            f"{self.base_url}/login",
            json={"email": email, "password": password},
        )

    @allure.step("Get current user profile")
    def get_me(self, token: str) -> requests.Response:
        return requests.get(
            f"{self.base_url}/me",
            headers={"Authorization": f"Bearer {token}"},
        )

    @allure.step("Get current user profile without token")
    def get_me_without_token(self) -> requests.Response:
        return requests.get(f"{self.base_url}/me")

    @allure.step("Get current user profile with invalid token")
    def get_me_with_invalid_token(self) -> requests.Response:
        return requests.get(
            f"{self.base_url}/me",
            headers={"Authorization": "Bearer invalid-token-12345"},
        )
