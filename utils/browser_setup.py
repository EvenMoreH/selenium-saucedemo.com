import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from utils.config import BASE_URL

@pytest.fixture(scope="function")
def driver():
    """
    Chrome WebDriver fixture with headless configuration.
    Automatically navigates to BASE_URL and cleans up after tests.
    """
    # set options
    options = Options()
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--start-maximized")
    options.add_argument("--incognito")
    options.add_argument("--headless")

    # initialize driver
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    driver.get(BASE_URL)

    yield driver

    # teardown
    driver.quit()