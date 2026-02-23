import allure
import requests
from config.config import BASE_URL


class CartApi:
    def __init__(self):
        self.base_url = f"{BASE_URL}/api/cart"

    @allure.step("Get cart")
    def get_cart(self, token: str) -> requests.Response:
        return requests.get(
            self.base_url,
            headers={"Authorization": f"Bearer {token}"},
        )

    @allure.step("Add item to cart: product_id={product_id}, quantity={quantity}")
    def add_item(self, token: str, product_id: int, quantity: int) -> requests.Response:
        return requests.post(
            f"{self.base_url}/items",
            json={"product_id": product_id, "quantity": quantity},
            headers={"Authorization": f"Bearer {token}"},
        )

    @allure.step("Add item to cart without auth")
    def add_item_without_auth(self, product_id: int, quantity: int) -> requests.Response:
        return requests.post(
            f"{self.base_url}/items",
            json={"product_id": product_id, "quantity": quantity},
        )

    @allure.step("Update cart item {item_id} quantity to {quantity}")
    def update_item(self, token: str, item_id: int, quantity: int) -> requests.Response:
        return requests.put(
            f"{self.base_url}/items/{item_id}",
            json={"quantity": quantity},
            headers={"Authorization": f"Bearer {token}"},
        )

    @allure.step("Delete cart item {item_id}")
    def delete_item(self, token: str, item_id: int) -> requests.Response:
        return requests.delete(
            f"{self.base_url}/items/{item_id}",
            headers={"Authorization": f"Bearer {token}"},
        )

    @allure.step("Clear cart")
    def clear_cart(self, token: str) -> requests.Response:
        return requests.delete(
            self.base_url,
            headers={"Authorization": f"Bearer {token}"},
        )
