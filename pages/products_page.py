from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver   # import to have intellisense inside methods
from selenium.common.exceptions import NoSuchElementException

class ProductsPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.shopping_cart = (By.CLASS_NAME, "shopping_cart_link")

        # self.sort_funnel = (By.CLASS_NAME, "product_sort_container")

    def open_cart(self):
        self.driver.find_element(*self.shopping_cart).click()

    def add_to_cart(self, product_id: str):
        try:
            # dynamic locator defined in method to not repeat it in __innit__
            add_to_cart_button = (By.ID, f"add-to-cart-{product_id}")
            # variable unpacked directly as it is in scope of the method
            self.driver.find_element(*add_to_cart_button).click()
        except NoSuchElementException:
            return False

    def is_in_cart(self, product_id: str):
        try:
            remove_from_cart_button = (By.ID, f"remove-{product_id}")
            # returning if remove button is displayed
            return self.driver.find_element(*remove_from_cart_button).is_displayed()
        except NoSuchElementException:
            return False

    def remove_from_cart(self, product_id: str):
        try:
            remover_from_cart_button = (By.ID, f"remove-{product_id}")
            self.driver.find_element(*remover_from_cart_button).click()
        except NoSuchElementException:
            return False

    def is_add_to_cart_button_visible(self, product_id: str):
        try:
            add_to_cart_button = (By.ID, f"add-to-cart-{product_id}")
            return self.driver.find_element(*add_to_cart_button).is_displayed()
        except NoSuchElementException:
            return False