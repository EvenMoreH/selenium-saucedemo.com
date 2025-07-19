import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from utils.config import BASE_URL

@pytest.fixture(scope="function")
def driver():
    # set options
    options = Options()
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--headless")
    options.add_argument("--start-maximized")

    # initialize driver
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    driver.get(BASE_URL)

    yield driver

    # teardown
    driver.quit()