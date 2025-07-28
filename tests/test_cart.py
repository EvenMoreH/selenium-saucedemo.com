import pytest
from utils.config import BASE_URL
from utils.browser_setup import driver
from pages.cart_page import Cart
from pages.products_page import ProductsPage
from utils.product_data import PRODUCT_IDS


@pytest.mark.cart
def test_continue_shopping_button(open_cart_page):
    current_user, driver = open_cart_page
    cart_page = Cart(driver)

    starting_url = driver.current_url

    cart_page.return_to_products_page()
    new_products_page_url = f"{BASE_URL}inventory.html"

    assert driver.current_url == new_products_page_url, (
        f"{current_user} started at: {starting_url}. "
        f"Expected redirection to: {new_products_page_url}. "
        f"{current_user} actually redirected to {driver.current_url}. "
    )

@pytest.mark.cart
@pytest.mark.parametrize("product_id", PRODUCT_IDS)
def test_remove_from_cart_on_cart_page(var_user_logged, product_id):
    current_user, driver = var_user_logged
    products_page = ProductsPage(driver)
    cart_page = Cart(driver)

    # Step 1: Add product and go to cart
    products_page.add_to_cart(product_id)
    products_page.open_cart()

    # Step 2: Check if items were added
    assert cart_page.is_in_cart(product_id), (
        f"Expected {product_id} to be in cart, but {current_user} could not add it. "
    )

    # Step 3: Remove items
    cart_page.remove_from_cart(product_id)

    # Step 4: Check if items were removed correctly
    assert not cart_page.is_in_cart(product_id), (
        f"Expected {product_id} to be removed from cart but it is still present. "
        )