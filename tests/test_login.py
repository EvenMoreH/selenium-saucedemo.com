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

@pytest.mark.login_page
@pytest.mark.parametrize(
    "username, password, should_succeed", [
        pytest.param("", TestUsers.standard["password"], False, id="Empty username"),
        pytest.param(TestUsers.standard["username"], "", False, id="Empty password"),
        pytest.param("", "", False, id="Empty username & password"),
    ]
)
def test_empty_fields_login(driver, username, password, should_succeed):
    """
    Tests login functionality with empty username and/or password fields.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        username (str): The username to be tested.
        password (str): The password to be tested.
        should_succeed (bool): Indicates whether the login should succeed.
    """
    login_page = LoginPage(driver)
    login_page.login(username, password)

    if should_succeed:
        assert driver.current_url == f"{BASE_URL}inventory.html", (
            "Login succeeded with empty username and/or password, but it should have failed."
        )
    else:
        assert not driver.current_url == f"{BASE_URL}inventory.html", (
            "Expected login failure but succeeded."
        )

@pytest.mark.login_page
@pytest.mark.parametrize(
    "username, password, should_succeed", [
        (TestUsers.standard["username"], " " + TestUsers.standard["password"], False),         # leading space - password
        (TestUsers.standard["username"], TestUsers.standard["password"] + " ", False),         # trailing space - password
        (TestUsers.standard["username"], " " + TestUsers.standard["password"] + " ", False),   # leading & trailing space - password
        (" " + TestUsers.standard["username"], TestUsers.standard["password"], False),         # leading space - username
        (TestUsers.standard["username"] + " ", TestUsers.standard["password"], False),         # trailing space - username
        (" " + TestUsers.standard["username"] + " ", TestUsers.standard["password"], False),   # leading & trailing space - username
    ]
)
def test_whitespace_login(driver, username, password, should_succeed):
    """
    Tests login functionality with whitespace around the username or password.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        username (str): The username to be tested.
        password (str): The password to be tested.
        should_succeed (bool): Indicates whether the login should succeed.
    """
    login_page = LoginPage(driver)
    login_page.login(username, password)

    if should_succeed:
        assert driver.current_url == f"{BASE_URL}inventory.html", (
            f"Expected successful login, but failed for {username}"
        )
    else:
        assert not driver.current_url == f"{BASE_URL}inventory.html", (
            f"Expected login failure but succeeded for {username}"
        )
        assert login_page.get_login_error_message() == "Epic sadface: Username and password do not match any user in this service"

@pytest.mark.login_page
@pytest.mark.parametrize(
    "username, password, should_succeed", [
        (TestUsers.standard["username"].lower(), TestUsers.standard["password"], True),
        (TestUsers.standard["username"].upper(), TestUsers.standard["password"], False),
        (TestUsers.standard["username"].title(), TestUsers.standard["password"], False),
        (TestUsers.standard["username"].capitalize(), TestUsers.standard["password"], False),
    ]
)
def test_case_sensitive_login(driver, username, password, should_succeed):
    """
    Test login functionality with different username casing to validate case sensitivity handling.

    This test verifies how the application handles usernames with altered casing.
    It assumes the application's authentication schema treats usernames in a case-insensitive manner for lowercase inputs,
    but is expected to fail for other casing variations (uppercase, titlecase, etc.).

    Passwords are NOT mutated in this test because passwords are required to be fully case-sensitive
    by security standards. Altering password casing would always result in a failure,
    which is not valuable for this specific case sensitivity validation of usernames.
    """
    login_page = LoginPage(driver)
    login_page.login(username, password)

    if should_succeed:
        assert driver.current_url == f"{BASE_URL}inventory.html", (
            f"Expected successful login. ",
            f"Login failed for user: {username}."
        )
    else:
        assert not driver.current_url == f"{BASE_URL}inventory.html", (
            f"Expected login fail. ",
            f"{username} was able to log in using incorrect case."
        )