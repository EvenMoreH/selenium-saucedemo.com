import pytest
from utils.product_data import PRODUCT_IDS
from utils.browser_setup import driver
from pages.products_page import ProductsPage
from pages.product_details_page import ProductDetails

@pytest.mark.cart
@pytest.mark.parametrize("product_id", PRODUCT_IDS)
def test_add_to_cart(var_user_logged, product_id):
    """
    Tests adding a product to the shopping cart from product details page.

    Args:
        var_user_logged: A tuple containing the current user and WebDriver instance.
        product_id: The ID of the product to be added to the cart.
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

def test_remove_from_cart():
    pass


def test_check_item_price():
    pass


def test_check_product_img():
    pass

