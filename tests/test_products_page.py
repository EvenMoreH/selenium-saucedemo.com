import pytest
from utils.browser_setup import driver
from pages.products_page import ProductsPage
from utils.product_data import PRODUCT_IDS
from utils.config import SOCIAL_MEDIA
from selenium.webdriver.support.ui import WebDriverWait
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
def test_sort_za(var_user_logged):
    current_user, driver = var_user_logged
    products_page = ProductsPage(driver)
    products_page.sort_za()

    current_products_order = products_page.capture_all_products_name()
    expected_products_order = sorted(PRODUCT_IDS, reverse=True)

    assert current_products_order == expected_products_order, (
        f"After AZ sort, expected list of products: {expected_products_order}. "
        f"{current_user} got: {current_products_order}. "
    )

@pytest.mark.filter
def test_sort_az(var_user_logged):
    current_user, driver = var_user_logged
    products_page = ProductsPage(driver)
    # Step 1: Force Z-A sort
    products_page.sort_za()
    current_za_order = products_page.capture_all_products_name()

    assert current_za_order == sorted(PRODUCT_IDS, reverse=True), (
        f"Step 1: Sort items Z-A failed for {current_user}. "
        "Test interrupted. "
    )

    # Step 2: Test A-Z sort
    products_page.sort_az()

    current_az_order = products_page.capture_all_products_name()
    expected_products_order = sorted(PRODUCT_IDS)

    assert current_az_order == expected_products_order, (
        f"After AZ sort, expected list of products: {expected_products_order}. "
        f"{current_user} got: {current_az_order}. "
    )

@pytest.mark.filter
def test_sort_high_low(var_user_logged):
    current_user, driver = var_user_logged
    products_page = ProductsPage(driver)

    expected_product_order = products_page.capture_all_products_price()
    expected_product_order = sorted(expected_product_order, reverse=True)

    products_page.sort_high_low()
    current_product_order = products_page.capture_all_products_price()

    assert current_product_order == expected_product_order, (
        f"After high to low price sort, expected list of products: {expected_product_order}. "
        f"{current_user} got: {current_product_order}. "
    )

@pytest.mark.filter
def test_sort_low_high(var_user_logged):
    current_user, driver = var_user_logged
    products_page = ProductsPage(driver)

    expected_product_order = products_page.capture_all_products_price()
    expected_product_order = sorted(expected_product_order)

    products_page.sort_low_high()
    current_products_order = products_page.capture_all_products_price()

    assert current_products_order == expected_product_order, (
        f"After low to high price sort, expected list of products: {expected_product_order}. "
        f"{current_user} got: {current_products_order}. "
    )

@pytest.mark.social
def test_social_media_link(var_user_logged):
    current_user, driver = var_user_logged
    products_page = ProductsPage(driver)

    products_page.visit_linkedin()

    WebDriverWait(driver, 5).until(
        lambda d: len(d.window_handles) > 1
    )
    driver.switch_to.window(driver.window_handles[1])

    assert driver.current_url == SOCIAL_MEDIA, (
        f"Expected arrival at url: {SOCIAL_MEDIA}, {current_user} actually redirected to: {driver.current_url}. "
    )