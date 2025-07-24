# shared fixtures for all test files
import pytest
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from utils.config import TestUsers

@pytest.fixture
def default_user_logged(driver):
    login_page = LoginPage(driver)
    login_page.login(**TestUsers.standard)
    return driver

@pytest.fixture(params=[
    ("standard_user", TestUsers.standard),
    ("problem_user", TestUsers.problem),
    ])
def var_user_logged(driver, request):
    login_page = LoginPage(driver)
    # unpacking tuple in correct order
    current_user, user_credentials = request.param
    login_page.login(**user_credentials)
    return current_user, driver

@pytest.fixture
def open_cart_page(var_user_logged):
    current_user, driver = var_user_logged
    products_page = ProductsPage(driver)
    products_page.open_cart()
    return current_user, driver