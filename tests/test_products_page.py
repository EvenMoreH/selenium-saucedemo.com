import pytest
from utils.browser_setup import driver
from pages.products_page import ProductsPage
from utils.product_data import PRODUCT_IDS
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


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
@pytest.mark.parametrize("product_id", PRODUCT_IDS)
def test_add_to_cart(var_user_logged, product_id):
    # unpacking var_user_logged return value in correct order
    current_user, driver = var_user_logged
    products_page = ProductsPage(driver)
    products_page.add_to_cart(product_id)
    # for clean demo output instead of standard assertion that would show whole traceback
    if not products_page.is_in_cart(product_id):
        pytest.fail(f"Expected {product_id} to be in cart, but {current_user} could not add it.")
    # assert products_page.is_in_cart(product_id), f"Expected {product_id} to be in cart, but {current_user} could not add it."

@pytest.mark.cart
@pytest.mark.parametrize("product_id", PRODUCT_IDS)
def test_remove_from_cart(var_user_logged, product_id):
    current_user, driver = var_user_logged
    products_page = ProductsPage(driver)
    products_page.add_to_cart(product_id)
    products_page.remove_from_cart(product_id)
    assert products_page.is_add_to_cart_button_visible(product_id), (
        f"Expected 'Add to cart' button to be visible for product {product_id} after removal. "
        f"{current_user} could not remove the product."
    )

@pytest.mark.cart
def test_cart_badge_increments(var_user_logged):
    current_user, driver = var_user_logged
    products_page = ProductsPage(driver)

    initial_count = products_page.cart_badge_count()

    for product_index, product_id in enumerate(PRODUCT_IDS, start=1):
        products_page.add_to_cart(product_id)
        expected_count = initial_count + product_index

        try:
            WebDriverWait(driver, 5).until(
                lambda d: ProductsPage(d).cart_badge_count() == expected_count
            )
        except TimeoutException:
            actual_count = ProductsPage(driver).cart_badge_count()
            raise AssertionError(
                f"Timeout, expected: {expected_count} items in cart, but got: {actual_count} for {current_user}."
            )

        assert products_page.cart_badge_count() == expected_count, (
            f"Expected cart badge to show {expected_count}, after adding {product_index} products to cart, "
            f"but got {products_page.cart_badge_count()}. Failed at product: {product_id} for user: {current_user}."
        )

@pytest.mark.filter
def test_sort_za(default_user_logged):
    driver = default_user_logged
    products_page = ProductsPage(driver)
    products_page.sort_za()
    # TODO: Assertion that validates sorting

@pytest.mark.filter
def test_sort_az(default_user_logged):
    driver = default_user_logged
    products_page = ProductsPage(driver)
    products_page.sort_az()
    # TODO: Assertion that validates sorting

@pytest.mark.filter
def test_sort_high_low(default_user_logged):
    driver = default_user_logged
    products_page = ProductsPage(driver)
    products_page.sort_high_low()
    # TODO: Assertion that validates sorting

@pytest.mark.filter
def test_sort_low_high(default_user_logged):
    driver = default_user_logged
    products_page = ProductsPage(driver)
    products_page.sort_low_high()
    # TODO: Assertion that validates sorting