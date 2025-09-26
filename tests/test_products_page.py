import pytest
from utils.browser_setup import driver
from pages.products_page import ProductsPage
from pages.product_details_page import ProductDetails
from utils.product_data import PRODUCT_IDS
from utils.product_data import PRODUCT_NAMES
from utils.product_data import PRODUCT_PRICES
from utils.config import BASE_URL
from utils.config import SOCIAL_MEDIA
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


@pytest.mark.smoke
def test_open_cart_default(default_user_logged):
    """
    Verify that the cart can be opened for a default user.

    Args:
        default_user_logged (WebDriver): WebDriver instance with a default user logged in.

    Assertions:
        - Current URL matches the expected cart URL.
    """
    products_page = ProductsPage(default_user_logged)
    products_page.open_cart()
    assert default_user_logged.current_url == f"{BASE_URL}cart.html"

@pytest.mark.cart
def test_open_cart_var(var_user_logged):
    """
    Verify that the cart can be opened for variable users (standard and problem).

    Args:
        var_user_logged (tuple): (str, WebDriver) - Username and WebDriver instance with variable user logged in.

    Assertions:
        - Current URL matches the expected cart URL.
    """
    current_user, driver = var_user_logged
    products_page = ProductsPage(driver)
    products_page.open_cart()
    # using driver instead function name, as return values were already unpacked
    assert driver.current_url == f"{BASE_URL}cart.html", f"{current_user} could not access cart."


@pytest.mark.cart
@pytest.mark.parametrize("product_id", PRODUCT_IDS)
def test_add_to_cart(var_user_logged, product_id):
    """
    Verify that a product can be added to the cart for variable users.

    Args:
        var_user_logged (tuple): (str, WebDriver) - Username and WebDriver instance with variable user logged in.
        product_id (str): ID of the product to be added to the cart.

    Assertions:
        - Product is successfully added to the cart.
    """
    # unpacking var_user_logged return value in correct order
    current_user, driver = var_user_logged
    products_page = ProductsPage(driver)
    products_page.add_to_cart(product_id)
    assert products_page.is_in_cart(product_id), f"Expected {product_id} to be in cart, but {current_user} could not add it."

@pytest.mark.cart
@pytest.mark.parametrize("product_id", PRODUCT_IDS)
def test_remove_from_cart(var_user_logged, product_id):
    """
    Verify that a product can be removed from the cart for variable users.

    Args:
        var_user_logged (tuple): (str, WebDriver) - Username and WebDriver instance with variable user logged in.
        product_id (str): ID of the product to be added and removed from the cart.

    Assertions:
        - 'Add to cart' button is visible for the removed product.
    """
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
    """
    Verify that the cart badge count increments correctly when adding multiple products.

    Args:
        var_user_logged (tuple): (str, WebDriver) - Username and WebDriver instance with variable user logged in.

    Assertions:
        - Cart badge count matches the expected count after adding each product.
    """
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

@pytest.mark.price
@pytest.mark.parametrize("product_id", PRODUCT_IDS)
def test_check_price(var_user_logged, product_id):
    """
    Verify that product prices match the expected values.

    Args:
        var_user_logged (tuple): (str, WebDriver) - Username and WebDriver instance with variable user logged in.
        product_id (str): Unique identifier of the product to check.

    Assertions:
        - Product name exists in PRODUCT_PRICES and price matches expected value.
    """
    current_user, driver = var_user_logged
    products_page = ProductsPage(driver)

    name, price = products_page.get_product_item(product_id)

    assert name in PRODUCT_PRICES and PRODUCT_PRICES[name] == price, (
        f"Expected {product_id} with correct price. "
        f"Instead {current_user} got incorrect price, or item/price was not found on the page."
    )

def test_check_product_description():
    pass


@pytest.mark.filter
def test_sort_za(var_user_logged):
    """
    Verify that products can be sorted in descending order (Z-A).

    Args:
        var_user_logged (tuple): (str, WebDriver) - Username and WebDriver instance with variable user logged in.

    Assertions:
        - Current product order matches the expected Z-A sorted order.
    """
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
    """
    Verify that products can be sorted in ascending order (A-Z).

    Args:
        var_user_logged (tuple): (str, WebDriver) - Username and WebDriver instance with variable user logged in.

    Assertions:
        - Initial Z-A sort works correctly.
        - Final A-Z sort matches the expected order.
    """
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
    """
    Verify that products can be sorted by price in descending order (high to low).

    Args:
        var_user_logged (tuple): (str, WebDriver) - Username and WebDriver instance with variable user logged in.

    Assertions:
        - Current product price order matches the expected high to low sorted order.
    """
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
    """
    Verify that products can be sorted by price in ascending order (low to high).

    Args:
        var_user_logged (tuple): (str, WebDriver) - Username and WebDriver instance with variable user logged in.

    Assertions:
        - Current product price order matches the expected low to high sorted order.
    """
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
    """
    Verify that the LinkedIn social media link can be accessed.

    Args:
        var_user_logged (tuple): (str, WebDriver) - Username and WebDriver instance with variable user logged in.

    Assertions:
        - New tab is opened after clicking LinkedIn link.
        - Current URL matches the expected LinkedIn URL.
    """
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

@pytest.mark.details
@pytest.mark.parametrize("product_id", PRODUCT_IDS)
def test_open_product_details(var_user_logged, product_id):
    """
    Verify opening a product details page and displayed product name.

    Args:
        var_user_logged (tuple): (str, WebDriver) - Username and WebDriver instance with variable user logged in.
        product_id (str): ID of the product to be opened.

    Assertions:
        - Product details page displays the correct product name.
    """
    current_user, driver = var_user_logged
    products_page = ProductsPage(driver)
    product_details_page = ProductDetails(driver)

    products_page.open_product_details(product_id)

    assert product_details_page.capture_product_name() == product_id, (
        f"Expected product details for: {product_id}. "
        f"{current_user} sees: {product_details_page.capture_product_name()}. "
    )


@pytest.mark.img
@pytest.mark.parametrize("product_id", PRODUCT_IDS)
def test_check_product_img(var_user_logged, product_id):
    # for demo purposes I will not be using PIL & hashlib nor visual comparison libraries to validate the img
    """
    Verify that product images are correctly displayed on the products page.

    Args:
        var_user_logged (tuple): (str, WebDriver) - Username and WebDriver instance with variable user
            logged in.
        product_id (str): ID of the product whose image should be checked.

    Assertions:
        - Product image is displayed in the UI.
        - Product image has a non-empty source attribute.
    """
    current_user, driver = var_user_logged
    products_page = ProductsPage(driver)

    img, img_src = products_page.capture_product_img(product_id)

    assert img.is_displayed(), (
        f"Expected product img to be displayed. {current_user} does not see the img."
    )

    assert img_src is not None and img_src != "", (
        f"Expected img source to not be empty. Img source empty for {current_user}."
    )