# from utils.browser_setup import driver
import pytest
from utils.browser_setup import driver
from pages.login_page import LoginPage
from utils.config import TestUsers

@pytest.mark.login_page
def test_valid_login(driver):
    login_page = LoginPage(driver)
    login_page.login(**TestUsers.standard)
    assert driver.current_url == "https://www.saucedemo.com/inventory.html"

@pytest.mark.login_page
def test_invalid_login(driver):
    login_page = LoginPage(driver)
    login_page.login(**TestUsers.incorrect)
    assert login_page.get_error_message() == "Epic sadface: Username and password do not match any user in this service"

@pytest.mark.login_page
def test_locked_out_login(driver):
    login_page = LoginPage(driver)
    login_page.login(**TestUsers.locked)
    assert login_page.get_error_message() == "Epic sadface: Sorry, this user has been locked out."