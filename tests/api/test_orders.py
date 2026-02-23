import allure
import pytest

from helpers.auth_helper import AuthHelper


@allure.epic("Shop API")
@allure.feature("Orders")
class TestOrders:

    @pytest.fixture(autouse=True)
    def setup(self, cart_api, order_api):
        self.user_token = AuthHelper.register_and_get_token()
        self.admin_token = AuthHelper.get_admin_token()
        self.cart_api = cart_api
        self.order_api = order_api

    def _create_order(self, token, product_id):
        self.cart_api.add_item(token, product_id, 1)
        return self.order_api.create_order(token)

    @allure.story("Create Order")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("Create order from cart with items")
    def test_create_order_from_cart(self, test_product):
        response = self._create_order(self.user_token, test_product["id"])

        assert response.status_code == 201
        body = response.json()
        assert body["id"] is not None
        assert body["status"] == "pending"
        assert body["total"] > 0
        assert len(body["items"]) == 1
        assert body["items"][0]["product_id"] is not None
        assert body["items"][0]["quantity"] is not None
        assert body["items"][0]["price"] is not None

    @allure.story("Create Order")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Creating order from empty cart is rejected")
    def test_create_order_from_empty_cart(self):
        response = self.order_api.create_order(self.user_token)

        assert response.status_code == 400

    @allure.story("Create Order")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Cart is empty after creating order")
    def test_cart_empty_after_order(self, test_product):
        self._create_order(self.user_token, test_product["id"])

        cart_response = self.cart_api.get_cart(self.user_token)
        body = cart_response.json()
        assert cart_response.status_code == 200
        assert len(body["items"]) == 0
        assert body["total"] == 0

    @allure.story("View Orders")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("Get user orders list")
    def test_get_orders_list(self, test_product):
        create_response = self._create_order(self.user_token, test_product["id"])
        order_id = create_response.json()["id"]

        response = self.order_api.get_orders(self.user_token)

        assert response.status_code == 200
        order_ids = [o["id"] for o in response.json()]
        assert order_id in order_ids

    @allure.story("View Orders")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Get order by ID")
    def test_get_order_by_id(self, test_product):
        create_response = self._create_order(self.user_token, test_product["id"])
        order_id = create_response.json()["id"]

        response = self.order_api.get_order(self.user_token, order_id)

        assert response.status_code == 200
        body = response.json()
        assert body["id"] == order_id
        assert body["status"] == "pending"
        assert body["total"] is not None
        assert body["user_id"] is not None
        assert body["created_at"] is not None
        assert body["items"] is not None

    @allure.story("View Orders")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("User cannot access other user's order")
    def test_get_other_user_order(self, test_product):
        create_response = self._create_order(self.user_token, test_product["id"])
        order_id = create_response.json()["id"]

        other_token = AuthHelper.register_and_get_token()
        response = self.order_api.get_order(other_token, order_id)

        assert response.status_code == 404

    @allure.story("Admin Orders")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Admin can get all orders")
    def test_admin_get_all_orders(self, test_product):
        self._create_order(self.user_token, test_product["id"])

        response = self.order_api.get_admin_orders(self.admin_token)

        assert response.status_code == 200
        assert len(response.json()) > 0

    @allure.story("Admin Orders")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Admin can update order status to confirmed")
    def test_admin_update_status_to_confirmed(self, test_product):
        create_response = self._create_order(self.user_token, test_product["id"])
        order_id = create_response.json()["id"]

        response = self.order_api.update_order_status(self.admin_token, order_id, "confirmed")

        assert response.status_code == 200
        assert response.json()["status"] == "confirmed"

    @allure.story("Admin Orders")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Invalid status transition is rejected")
    def test_admin_invalid_status_transition(self, test_product):
        create_response = self._create_order(self.user_token, test_product["id"])
        order_id = create_response.json()["id"]

        response = self.order_api.update_order_status(self.admin_token, order_id, "delivered")

        assert response.status_code == 400

    @allure.story("Admin Orders")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Regular user cannot update order status")
    def test_user_cannot_update_status(self, test_product):
        create_response = self._create_order(self.user_token, test_product["id"])
        order_id = create_response.json()["id"]

        response = self.order_api.update_order_status(self.user_token, order_id, "confirmed")

        assert response.status_code == 403
