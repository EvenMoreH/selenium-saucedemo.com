import pytest
from utils.config import BASE_URL
from utils.browser_setup import driver
from pages.cart_page import Cart
from pages.products_page import ProductsPage
from utils.product_data import PRODUCT_IDS


@pytest.mark.cart
def test_continue_shopping_button(open_cart_page):
    """
    Verify the 'Continue Shopping' button redirects to the products page.

    Args:
        open_cart_page (tuple): (str, WebDriver) - Username and WebDriver instance with cart page opened.

    Assertions:
        - Current URL matches the expected products page URL after clicking 'Continue Shopping'.
    """
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
    """
    Verify that a product can be removed from the cart page.

    Args:
        var_user_logged (tuple): (str, WebDriver) - Username and WebDriver instance with variable user logged in.
        product_id (str): ID of the product to be added and removed from the cart.

    Assertions:
        - Product is present in the cart after adding.
        - Product is no longer in the cart after removal.
    """
    current_user, driver = var_user_logged
    products_page = ProductsPage(driver)
    cart_page = Cart(driver)

    # Step 1: Add product and go to cart
    products_page.add_to_cart(product_id)
    products_page.open_cart()

    # Step 2: Check if item was added
    assert cart_page.is_in_cart(product_id), (
        f"Expected {product_id} to be in cart, but {current_user} could not add it. "
    )

    # Step 3: Remove item
    cart_page.remove_from_cart(product_id)

    # Step 4: Check if item was removed correctly
    assert not cart_page.is_in_cart(product_id), (
        f"Expected {product_id} to be removed from cart but it is still present. "
        )

@pytest.mark.cart
def test_add_and_remove_multiple_items(var_user_logged):
    """
    Verify that multiple products can be added and then removed from the cart.

    Args:
        var_user_logged (tuple): (str, WebDriver) - Username and WebDriver instance with variable user logged in.

    Assertions:
        - All products are present in the cart after adding.
        - Cart is empty after removing all products.
    """
    current_user, driver = var_user_logged
    products_page = ProductsPage(driver)
    cart_page = Cart(driver)

    # Step 1: Add all products
    for product_id in PRODUCT_IDS:
        products_page.add_to_cart(product_id)

    # Step 2: Go to cart page
    products_page.open_cart()

    # Step 3: Confirm all products are in cart
    for product_id in PRODUCT_IDS:
        assert cart_page.is_in_cart(product_id), f"{product_id} missing from cart for {current_user}. "

    # Step 4: Remove all products from cart
    for product_id in PRODUCT_IDS:
        cart_page.remove_from_cart(product_id)

    # Step 5: Confirm cart is empty
    for product_id in PRODUCT_IDS:
        assert not cart_page.is_in_cart(product_id), f"{product_id} was not removed for {current_user}. "

@pytest.mark.cart
def test_checkout_btn(var_user_logged):
    """
    Verify redirection to the checkout page when clicking the checkout button.

    Args:
        var_user_logged (tuple): (str, WebDriver) - Username and WebDriver instance with variable user logged in.

    Assertions:
        - Current URL matches the expected checkout page URL.
    """
    current_user, driver = var_user_logged
    products_page = ProductsPage(driver)
    cart_page = Cart(driver)

    products_page.open_cart()
    cart_page.click_checkout_btn()
    expected_url = f"{BASE_URL}checkout-step-one.html"

    assert driver.current_url == expected_url, (
        f"Expected {current_user} to be redirected to: {expected_url} ."
        f"{current_user} actually redirected to {driver.current_url}."
    )