from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver   # import to have intellisense inside methods
from selenium.common.exceptions import NoSuchElementException

class Cart:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.continue_shopping_btn = (By.ID, "continue-shopping")
        self.checkout_btn = (By.ID, "checkout")

    def return_to_products_page(self):
        self.driver.find_element(*self.continue_shopping_btn).click()