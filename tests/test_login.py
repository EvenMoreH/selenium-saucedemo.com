# from utils.browser_setup import driver
from utils.browser_setup import driver
from pages.login_page import LoginPage
from utils.config import TEST_USER, TEST_PASS

def test_valid_login(driver):
    login_page = LoginPage(driver)
    login_page.login(TEST_USER, TEST_PASS)
    assert driver.current_url == "https://www.saucedemo.com/inventory.html"