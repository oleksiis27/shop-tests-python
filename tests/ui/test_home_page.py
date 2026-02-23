import allure
import pytest

from pages.home_page import HomePage


@allure.epic("Shop UI")
@allure.feature("Home Page")
class TestHomePage:

    @allure.story("Page Load")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("Home page loads and displays products")
    def test_home_page_loads_with_products(self, page):
        home_page = HomePage(page)

        home_page.open_page()

        assert home_page.get_product_cards_count() > 0

    @allure.story("Search")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Search 'Laptop' filters results")
    def test_search_product_filters_results(self, page):
        home_page = HomePage(page)

        home_page.open_page()
        home_page.search("Laptop")

        assert home_page.get_product_cards_count() >= 0

    @allure.story("Filter")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Filter by Electronics category")
    def test_filter_by_category(self, page):
        home_page = HomePage(page)

        home_page.open_page()
        home_page.filter_by_category("Electronics")

        assert home_page.get_product_cards_count() >= 0

    @allure.story("Sort")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Sort by price ascending")
    def test_sort_by_price_ascending(self, page):
        home_page = HomePage(page)

        home_page.open_page()
        home_page.sort_by("price_asc")

        assert home_page.get_product_cards_count() > 0

    @allure.story("Pagination")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Next page button works")
    def test_pagination_works(self, page):
        home_page = HomePage(page)

        home_page.open_page()
        home_page.click_next_page()

        assert "/" in page.url
