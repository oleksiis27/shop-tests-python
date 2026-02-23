from typing import Optional

import allure
import requests
from config.config import BASE_URL


class ProductApi:
    def __init__(self):
        self.base_url = f"{BASE_URL}/api/products"

    @allure.step("Get products list")
    def get_products(self, params: Optional[dict] = None) -> requests.Response:
        return requests.get(self.base_url, params=params)

    @allure.step("Get product by id: {product_id}")
    def get_product(self, product_id: int) -> requests.Response:
        return requests.get(f"{self.base_url}/{product_id}")

    @allure.step("Create product as admin")
    def create_product(self, token: str, body: dict) -> requests.Response:
        return requests.post(
            self.base_url,
            json=body,
            headers={"Authorization": f"Bearer {token}"},
        )

    @allure.step("Create product without auth")
    def create_product_without_auth(self, body: dict) -> requests.Response:
        return requests.post(self.base_url, json=body)

    @allure.step("Update product id: {product_id}")
    def update_product(self, token: str, product_id: int, body: dict) -> requests.Response:
        return requests.put(
            f"{self.base_url}/{product_id}",
            json=body,
            headers={"Authorization": f"Bearer {token}"},
        )

    @allure.step("Delete product id: {product_id}")
    def delete_product(self, token: str, product_id: int) -> requests.Response:
        return requests.delete(
            f"{self.base_url}/{product_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
