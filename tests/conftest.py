# shared fixtures for all test files
import pytest
from pages.login_page import LoginPage
from utils.config import TestUsers

@pytest.fixture
def default_user_logged(driver):
    login_page = LoginPage(driver)
    login_page.login(**TestUsers.standard)
    return driver

@pytest.fixture(params=[TestUsers.standard, TestUsers.problem])
def var_user_logged(driver, request):
    login_page = LoginPage(driver)
    user_credentials = request.param
    login_page.login(**user_credentials)
    return driver