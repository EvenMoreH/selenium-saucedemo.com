import pytest
from utils.config import BASE_URL
from utils.product_data import PRODUCT_IDS
from utils.product_data import PRODUCT_PRICES
from utils.browser_setup import driver
from pages.products_page import ProductsPage
from pages.product_details_page import ProductDetails

@pytest.mark.cart
@pytest.mark.parametrize("product_id", PRODUCT_IDS)
def test_add_to_cart(var_user_logged, product_id):
    """
    Verify adding a product to the shopping cart from product details page.

    Args:
        var_user_logged (tuple): (str, WebDriver) - Username and WebDriver instance with variable user logged in.
        product_id (str): ID of the product to be added to the cart.

    Assertions:
        - Product details page displays the correct product name.
        - Cart is initially empty for new shopping session.
        - Product is successfully added to cart.
    """
    current_user, driver = var_user_logged
    products_page = ProductsPage(driver)
    product_details_page = ProductDetails(driver)

    products_page.open_product_details(product_id)
    current_product = product_details_page.capture_product_name()

    assert product_details_page.capture_product_name() == product_id, (
        f"Expected product details for: {product_id}. "
        f"{current_user} sees: {current_product}. "
    )
    assert not product_details_page.is_in_cart(), (
        f"Expected empty cart for new {current_user} shopping session. "
    )

    product_details_page.add_to_cart()

    assert product_details_page.is_in_cart(), (
        f"Expected {current_user} to have {product_id} in cart. "
        f"{current_user} was not able to add {product_id} to cart."
    )

@pytest.mark.cart
@pytest.mark.parametrize("product_id", PRODUCT_IDS)
def test_remove_from_cart(var_user_logged, product_id):
    """
    Verify that a product can be removed from the cart from product details page.

    Args:
        var_user_logged (tuple): (str, WebDriver) - Username and WebDriver instance with variable user logged in.
        product_id (str): ID of the product to be tested.

    Assertions:
        - Redirection to the correct product details page URL.
        - Product is successfully added to the cart.
        - Product is successfully removed from the cart.
    """
    current_user, driver = var_user_logged
    products_page = ProductsPage(driver)
    product_details_page = ProductDetails(driver)

    products_page.add_to_cart(product_id)
    products_page.open_product_details(product_id)
    assert product_details_page.is_on_product_details_page(), (
        f"Expected redirection to product details page. "
        f"{current_user} redirected instead to {driver.current_url}."
    )

    assert product_details_page.is_in_cart(), (
        f"Expected {product_id} to be in cart, but {current_user} could not add it."
    )

    product_details_page.remove_from_cart()

    assert not product_details_page.is_in_cart(), (
        f"Expected 'Add to cart' button to be visible for product {product_id} after removal. "
        f"{current_user} could not remove the product."
    )


@pytest.mark.price
@pytest.mark.parametrize("product_id", PRODUCT_IDS)
def test_check_item_price(var_user_logged, product_id):
    """
    Verify the correctness of the item price on the product details page.

    Args:
        var_user_logged (tuple): (str, WebDriver) - Username and WebDriver instance with variable user logged in.
        product_id (str): ID of the product to be tested.

    Assertions:
        - Redirection to the correct product details page URL.
        - Product name and price match with expected values.
    """
    current_user, driver = var_user_logged
    products_page = ProductsPage(driver)
    product_details_page = ProductDetails(driver)

    products_page.open_product_details(product_id)
    assert product_details_page.is_on_product_details_page(), (
        f"Expected redirection to product details page. "
        f"{current_user} redirected instead to {driver.current_url}."
    )

    name, price = product_details_page.get_product_item(product_id)

    assert name in PRODUCT_PRICES and PRODUCT_PRICES[name] == price, (
        f"Expected {product_id} with correct price. "
        f"Instead {current_user} got incorrect price, or item/price was not found on the page."
    )


@pytest.mark.cart
@pytest.mark.parametrize("product_id", PRODUCT_IDS)
def test_return_to_products_page(var_user_logged, product_id):
    """
    Verify that the user returns correctly to the products page after viewing a product.

    Args:
        var_user_logged (tuple): (str, WebDriver) - Username and WebDriver instance with variable user logged in.
        product_id (str): ID of the product to be tested.

    Assertions:
        - Redirection to the correct product details page URL.
        - Correct redirection back to the products page after clicking 'Back to Products'.
    """
    current_user, driver = var_user_logged
    products_page = ProductsPage(driver)
    product_details_page = ProductDetails(driver)

    products_page.open_product_details(product_id)
    assert product_details_page.is_on_product_details_page(), (
        f"Expected redirection to product details page. "
        f"{current_user} redirected instead to {driver.current_url}."
    )

    product_details_page.click_back_to_products()
    assert driver.current_url == f"{BASE_URL}inventory.html", (
        f"Expected {current_user} to be redirected back to products page. "
        f"{current_user} instead redirected to {driver.current_url}."
    )

def test_check_product_img():
    # for demo purposes I will not be using PIL & hashlib nor visual comparison libraries to validate the img
    

    pass