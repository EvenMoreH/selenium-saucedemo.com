import pytest
from utils.browser_setup import driver
from utils.config import BASE_URL
from pages.login_page import LoginPage
from utils.config import TestUsers

@pytest.mark.login_page
def test_valid_login(driver):
    """
    Test logging in with valid credentials.

    This test verifies that a user can successfully log in using standard credentials.
    After logging in, it asserts that the current URL is the inventory page.

    :param driver: The Selenium WebDriver instance used for testing.
    """
    login_page = LoginPage(driver)
    login_page.login(**TestUsers.standard)
    assert driver.current_url == f"{BASE_URL}inventory.html"

@pytest.mark.login_page
def test_invalid_login(driver):
    """
    Test logging in with invalid credentials.

    This test verifies that an appropriate error message is displayed when attempting to log in with incorrect credentials.

    :param driver: The Selenium WebDriver instance used for testing.
    """
    login_page = LoginPage(driver)
    login_page.login(**TestUsers.incorrect)
    assert login_page.get_login_error_message() == "Epic sadface: Username and password do not match any user in this service"

@pytest.mark.login_page
def test_locked_out_login(driver):
    """
    Test logging in with locked out credentials.

    This test verifies that an appropriate error message is displayed when attempting to log in with a locked-out account.

    :param driver: The Selenium WebDriver instance used for testing.
    """
    login_page = LoginPage(driver)
    login_page.login(**TestUsers.locked)
    assert login_page.get_login_error_message() == "Epic sadface: Sorry, this user has been locked out."