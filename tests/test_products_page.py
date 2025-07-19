import pytest
from utils.browser_setup import driver
from pages.products_page import ProductsPage

@pytest.mark.cart
def test_open_cart_default(default_user_logged):
    products_page = ProductsPage(default_user_logged)
    products_page.open_cart()
    assert default_user_logged.current_url == "https://www.saucedemo.com/cart.html"

@pytest.mark.cart
def test_open_cart_var(var_user_logged):
    products_page = ProductsPage(var_user_logged)
    products_page.open_cart()
    assert var_user_logged.current_url == "https://www.saucedemo.com/cart.html"