import pytest
from utils.config import BASE_URL
from utils.browser_setup import driver
from pages.cart_page import Cart
from pages.products_page import ProductsPage
from utils.product_data import PRODUCT_IDS


@pytest.mark.cart
def test_continue_shopping_button(open_cart_page):
    """
    Test to verify the 'Continue Shopping' button redirects to the products page.

    Steps:
    1. Open the cart page.
    2. Click on the 'Continue Shopping' button.
    3. Assert that the current URL is the products page URL.

    Parameters:
        open_cart_page (tuple): A tuple containing the username and WebDriver instance with the cart page opened.

    Raises:
        AssertionError: If the current URL does not match the expected products page URL after clicking the 'Continue Shopping' button.
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
    Test to verify that a product can be removed from the cart page.

    Steps:
    1. Open the products page as a variable user.
    2. Add a specified product to the cart and navigate to the cart page.
    3. Assert that the product is in the cart.
    4. Remove the product from the cart.
    5. Assert that the product is no longer in the cart.

    Parameters:
        var_user_logged (tuple): A tuple containing the username and WebDriver instance with a variable user logged in.
        product_id (str): The ID of the product to be added and removed from the cart.

    Raises:
        AssertionError: If the product is not found in the cart or if it remains in the cart after removal.
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
    Test to verify that multiple products can be added and then removed from the cart.

    Steps:
    1. Open the products page as a variable user.
    2. Add all products in PRODUCT_IDS to the cart.
    3. Navigate to the cart page.
    4. Assert that all products are present in the cart.
    5. Remove all products from the cart.
    6. Assert that the cart is empty.

    Parameters:
        var_user_logged (tuple): A tuple containing the username and WebDriver instance with a variable user logged in.

    Raises:
        AssertionError: If any product is not added to the cart, or if any product remains in the cart after removal.
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
    Tests redirection to the checkout page when clicking the checkout button.

    Args:
        var_user_logged: A tuple containing the current user and WebDriver instance.
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