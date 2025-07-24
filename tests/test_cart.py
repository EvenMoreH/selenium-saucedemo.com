import pytest
from utils.config import BASE_URL
from utils.browser_setup import driver
from pages.cart_page import Cart


@pytest.mark.btn1
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