import allure
import requests
from config.config import BASE_URL


class OrderApi:
    def __init__(self):
        self.base_url = f"{BASE_URL}/api"

    @allure.step("Create order from cart")
    def create_order(self, token: str) -> requests.Response:
        return requests.post(
            f"{self.base_url}/orders",
            headers={"Authorization": f"Bearer {token}"},
        )

    @allure.step("Get user orders")
    def get_orders(self, token: str) -> requests.Response:
        return requests.get(
            f"{self.base_url}/orders",
            headers={"Authorization": f"Bearer {token}"},
        )

    @allure.step("Get order by id: {order_id}")
    def get_order(self, token: str, order_id: int) -> requests.Response:
        return requests.get(
            f"{self.base_url}/orders/{order_id}",
            headers={"Authorization": f"Bearer {token}"},
        )

    @allure.step("Admin: get all orders")
    def get_admin_orders(self, token: str) -> requests.Response:
        return requests.get(
            f"{self.base_url}/admin/orders",
            headers={"Authorization": f"Bearer {token}"},
        )

    @allure.step("Admin: update order {order_id} status to {status}")
    def update_order_status(self, token: str, order_id: int, status: str) -> requests.Response:
        return requests.put(
            f"{self.base_url}/admin/orders/{order_id}/status",
            json={"status": status},
            headers={"Authorization": f"Bearer {token}"},
        )
