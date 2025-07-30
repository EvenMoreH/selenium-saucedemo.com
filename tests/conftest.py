# shared fixtures for all test files
import pytest
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from utils.config import TestUsers
import logging


def pytest_configure(config):
    """
    Pytest built-in hook that runs once at the beginning of the test session.
    Used here to set up global logging configuration.
    """
    logging.basicConfig(
        filename='test_results.log',
        filemode='w',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest built-in hook that runs after each test function.
    Used here to log whether the test passed, failed, or was skipped.
    """
    # execute all other hooks to obtain the report object
    outcome = yield
    report = outcome.get_result()

    if report.when == 'call':  # only log actual test call, not setup/teardown
        if report.passed:
            logging.info(f"TEST PASSED: {item.name}")
        elif report.failed:
            logging.error(f"TEST FAILED: {item.name}")
        elif report.skipped:
            logging.warning(f"TEST SKIPPED: {item.name}")

@pytest.fixture
def default_user_logged(driver):
    """
    Fixture to log in a standard user.
    This fixture logs in using the credentials of a standard user and returns the driver object.

    Args:
        driver (WebDriver): The Selenium WebDriver instance to be used for automation.

    Returns:
        WebDriver: The WebDriver instance after logging in.
    """
    login_page = LoginPage(driver)
    login_page.login(**TestUsers.standard)
    return driver

@pytest.fixture(params=[
    ("standard_user", TestUsers.standard),
    ("problem_user", TestUsers.problem),
    ])
def var_user_logged(driver, request):
    """
    Fixture to log in a variable user.
    This fixture logs in using different types of users and returns the username along with the driver object.

    Args:
        driver (WebDriver): The Selenium WebDriver instance to be used for automation.
        request (SubRequest): Provides access to parameters and other fixtures.

    Returns:
        tuple: A tuple containing the current user's name and the WebDriver instance.
    """
    login_page = LoginPage(driver)
    # unpacking tuple in correct order
    current_user, user_credentials = request.param
    login_page.login(**user_credentials)
    return current_user, driver

@pytest.fixture
def open_cart_page(var_user_logged):
    """
    Fixture to open the cart page.
    This fixture navigates to the cart page after a variable user is logged in and returns the username along with the driver object.

    Args:
        var_user_logged (tuple): A tuple containing the current user's name and the WebDriver instance.

    Returns:
        tuple: A tuple containing the current user's name and the WebDriver instance after navigating to the cart page.
    """
    current_user, driver = var_user_logged
    products_page = ProductsPage(driver)
    products_page.open_cart()
    return current_user, driver