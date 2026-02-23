import allure
import pytest

from helpers.test_data_helper import TestDataHelper


@allure.epic("Shop API")
@allure.feature("Products")
class TestProducts:

    @allure.story("Product List")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("Get paginated products list")
    def test_get_products_list(self, product_api):
        response = product_api.get_products()

        assert response.status_code == 200
        body = response.json()
        assert len(body["items"]) > 0
        assert body["total"] > 0
        assert body["page"] == 1
        assert body["limit"] > 0
        assert body["pages"] > 0

    @allure.story("Product List")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Filter products by category_id=1")
    def test_filter_by_category(self, product_api):
        response = product_api.get_products({"category": 1})

        assert response.status_code == 200
        body = response.json()
        assert len(body["items"]) > 0
        for item in body["items"]:
            assert item["category_id"] == 1

    @allure.story("Product List")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Search products by name")
    def test_search_by_name(self, product_api):
        # Get first product name to use as search term
        all_response = product_api.get_products()
        first_product_name = all_response.json()["items"][0]["name"]
        search_term = first_product_name.split()[0]

        response = product_api.get_products({"search": search_term})

        assert response.status_code == 200
        body = response.json()
        assert len(body["items"]) > 0

    @allure.story("Product List")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Sort products by price ascending")
    def test_sort_by_price_asc(self, product_api):
        response = product_api.get_products({"sort_by": "price_asc"})

        assert response.status_code == 200
        items = response.json()["items"]
        prices = [item["price"] for item in items]
        assert prices == sorted(prices)

    @allure.story("Product List")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Sort products by price descending")
    def test_sort_by_price_desc(self, product_api):
        response = product_api.get_products({"sort_by": "price_desc"})

        assert response.status_code == 200
        items = response.json()["items"]
        prices = [item["price"] for item in items]
        assert prices == sorted(prices, reverse=True)

    @allure.story("Product Details")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("Get product by ID")
    def test_get_product_by_id(self, product_api, test_product):
        product_id = test_product["id"]
        response = product_api.get_product(product_id)

        assert response.status_code == 200
        body = response.json()
        assert body["id"] == product_id
        assert body["name"]
        assert body["price"] is not None
        assert body["stock"] is not None
        assert body["category_id"] is not None

    @allure.story("Product Details")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Get non-existent product returns 404")
    def test_get_non_existent_product(self, product_api):
        response = product_api.get_product(99999)

        assert response.status_code == 404

    @allure.story("Product Management")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Admin can create a product")
    def test_create_product_as_admin(self, product_api, admin_token):
        body = TestDataHelper.random_product()

        response = product_api.create_product(admin_token, body)

        assert response.status_code == 201
        data = response.json()
        assert data["id"] is not None
        assert data["name"] == body["name"]
        assert data["stock"] == body["stock"]

    @allure.story("Product Management")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Regular user cannot create a product")
    def test_create_product_as_user(self, product_api, user_token):
        body = TestDataHelper.random_product()

        response = product_api.create_product(user_token, body)

        assert response.status_code == 403

    @allure.story("Product Management")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Unauthenticated user cannot create a product")
    def test_create_product_without_auth(self, product_api):
        body = TestDataHelper.random_product()

        response = product_api.create_product_without_auth(body)

        assert response.status_code == 403

    @allure.story("Product Management")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Admin can update a product")
    def test_update_product_as_admin(self, product_api, admin_token):
        # Create product first
        create_body = TestDataHelper.random_product_high_stock()
        create_response = product_api.create_product(admin_token, create_body)
        product_id = create_response.json()["id"]

        # Update it
        response = product_api.update_product(admin_token, product_id, {"name": "Updated Product Name"})

        assert response.status_code == 200
        assert response.json()["name"] == "Updated Product Name"

    @allure.story("Product Management")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Admin can delete a product")
    def test_delete_product_as_admin(self, product_api, admin_token):
        # Create product first
        create_body = TestDataHelper.random_product_high_stock()
        create_response = product_api.create_product(admin_token, create_body)
        product_id = create_response.json()["id"]

        # Delete it
        response = product_api.delete_product(admin_token, product_id)
        assert response.status_code == 204

        # Verify it's gone
        get_response = product_api.get_product(product_id)
        assert get_response.status_code == 404

    @allure.story("Product Management")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Delete non-existent product returns 404")
    def test_delete_non_existent_product(self, product_api, admin_token):
        response = product_api.delete_product(admin_token, 99999)

        assert response.status_code == 404
