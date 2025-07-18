# shared fixtures for all test files
import pytest
from pages.login_page import LoginPage
from utils.config import TestUsers

@pytest.fixture
def authenticated_in_driver(driver):
    login_page = LoginPage(driver)
    login_page.login(**TestUsers.standard)
    return driver