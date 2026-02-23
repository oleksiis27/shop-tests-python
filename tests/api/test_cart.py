import allure
import pytest

from helpers.auth_helper import AuthHelper


@allure.epic("Shop API")
@allure.feature("Cart")
class TestCart:

    @pytest.fixture(autouse=True)
    def setup(self, cart_api):
        self.token = AuthHelper.register_and_get_token()
        self.cart_api = cart_api

    @allure.story("Add to Cart")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("Add product to cart")
    def test_add_item_to_cart(self, test_product):
        response = self.cart_api.add_item(self.token, test_product["id"], 2)

        assert response.status_code == 201
        body = response.json()
        assert body["id"] is not None
        assert body["product_id"] is not None
        assert body["quantity"] is not None
        assert body["product"] is not None

    @allure.story("View Cart")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("Get cart with item")
    def test_get_cart_with_item(self, test_product):
        self.cart_api.add_item(self.token, test_product["id"], 2)

        response = self.cart_api.get_cart(self.token)

        assert response.status_code == 200
        body = response.json()
        assert len(body["items"]) == 1
        assert body["items"][0]["product_id"] == test_product["id"]
        assert body["items"][0]["quantity"] == 2
        assert body["total"] > 0

    @allure.story("Add to Cart")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Adding same product increases quantity")
    def test_add_same_product_increases_quantity(self, test_product):
        self.cart_api.add_item(self.token, test_product["id"], 2)
        self.cart_api.add_item(self.token, test_product["id"], 3)

        response = self.cart_api.get_cart(self.token)

        assert response.status_code == 200
        body = response.json()
        assert len(body["items"]) == 1
        assert body["items"][0]["quantity"] == 5

    @allure.story("Update Cart")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Update cart item quantity")
    def test_update_item_quantity(self, test_product):
        add_response = self.cart_api.add_item(self.token, test_product["id"], 2)
        item_id = add_response.json()["id"]

        response = self.cart_api.update_item(self.token, item_id, 5)

        assert response.status_code == 200
        assert response.json()["quantity"] == 5

    @allure.story("Remove from Cart")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Delete single cart item")
    def test_delete_cart_item(self, test_product):
        add_response = self.cart_api.add_item(self.token, test_product["id"], 2)
        item_id = add_response.json()["id"]

        response = self.cart_api.delete_item(self.token, item_id)
        assert response.status_code == 204

        cart_response = self.cart_api.get_cart(self.token)
        assert len(cart_response.json()["items"]) == 0

    @allure.story("Remove from Cart")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Clear all items from cart")
    def test_clear_cart(self, test_product, test_product_2):
        self.cart_api.add_item(self.token, test_product["id"], 1)
        self.cart_api.add_item(self.token, test_product_2["id"], 1)

        response = self.cart_api.clear_cart(self.token)
        assert response.status_code == 204

        cart_response = self.cart_api.get_cart(self.token)
        body = cart_response.json()
        assert len(body["items"]) == 0
        assert body["total"] == 0

    @allure.story("Add to Cart")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Cannot add item without auth")
    def test_add_item_without_auth(self, cart_api, test_product):
        response = cart_api.add_item_without_auth(test_product["id"], 1)

        assert response.status_code == 403
