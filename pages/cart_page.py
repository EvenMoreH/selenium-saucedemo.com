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

    def is_in_cart(self, product_id: str):
        try:
            remove_from_cart_button = (By.ID, f"remove-{product_id}")
            # returning if remove button is displayed
            return self.driver.find_element(*remove_from_cart_button).is_displayed()
        except NoSuchElementException:
            return False

    def remove_from_cart(self, product_id: str):
        try:
            remove_from_cart_button = (By.ID, f"remove-{product_id}")
            self.driver.find_element(*remove_from_cart_button).click()
        except NoSuchElementException:
            return False