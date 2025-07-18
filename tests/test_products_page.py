import pytest
from utils.browser_setup import driver
from pages.products_page import ProductsPage

@pytest.mark.cart
def test_open_cart(authenticated_in_driver):
    products_page = ProductsPage(authenticated_in_driver)
    products_page.open_cart()
    assert authenticated_in_driver.current_url == "https://www.saucedemo.com/cart.html"