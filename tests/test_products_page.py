import pytest
from utils.browser_setup import driver
from pages.products_page import ProductsPage

@pytest.mark.smoke
def test_open_cart_default(default_user_logged):
    products_page = ProductsPage(default_user_logged)
    products_page.open_cart()
    assert default_user_logged.current_url == "https://www.saucedemo.com/cart.html"

@pytest.mark.cart
def test_open_cart_var(var_user_logged):
    current_user, driver = var_user_logged
    products_page = ProductsPage(driver)
    products_page.open_cart()
    # using driver instead function name, as return values were already unpacked
    assert driver.current_url == "https://www.saucedemo.com/cart.html", f"{current_user} could not access cart."


@pytest.mark.cart
@pytest.mark.parametrize("product_id", [
    "sauce-labs-backpack",
    "sauce-labs-bike-light",
    "sauce-labs-bolt-t-shirt",
    "sauce-labs-fleece-jacket",
    "sauce-labs-onesie",
    "test.allthethings()-t-shirt-(red)"
    ])
def test_add_to_cart(var_user_logged, product_id):
    # unpacking var_user_logged return value in correct order
    current_user, driver = var_user_logged
    products_page = ProductsPage(driver)
    products_page.add_to_cart(product_id)
    # for clean demo output instead of standard assertion that would show whole traceback
    if not products_page.is_in_cart(product_id):
        pytest.fail(f"Expected {product_id} to be in cart, but {current_user} could not add it.")
    # assert products_page.is_in_cart(product_id), f"Expected {product_id} to be in cart, but {current_user} could not add it."
