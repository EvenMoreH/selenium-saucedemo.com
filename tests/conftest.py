# shared fixtures for all test files
import pytest
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from utils.config import TestUsers
import logging
import re


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

def remove_ansi(text):
    """
    Removes ANSI escape sequences from the given text using re module.

    Parameters:
    text : str
        The input string that may contain ANSI escape sequences.

    Returns : str
        The input string with all ANSI escape sequences removed.

    Notes:
    ------
    ANSI escape sequences are used to add color and formatting to terminal output.
    Not needed in 'test_results.log' file.
    """
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to log the outcome of each test case (pass, fail, or skip) during test execution.

    Logs the test name and, in case of failure, also logs the exception type and message
    (e.g., AssertionError, Selenium exceptions), with ANSI color codes removed for readability.
    """
    # execute all other hooks to obtain the report object
    outcome = yield
    report = outcome.get_result()

    if report.when == 'call':  # only log actual test call, not setup/teardown
        if report.passed:
            logging.info(f"TEST PASSED: {item.name}")
        elif report.failed:
            logging.error(f"TEST FAILED: {item.name}")
            if call.excinfo:
                exc_type = call.excinfo.type.__name__
                exc_msg = str(call.excinfo.value)
                logging.error(remove_ansi(f"{exc_type}: {exc_msg}"))
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