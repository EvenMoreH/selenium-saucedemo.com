from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver   # import to have intellisense inside methods

class ProductsPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.shopping_cart = (By.CLASS_NAME, "shopping_cart_link")

        # self.sort_funnel = (By.CLASS_NAME, "product_sort_container")

    def open_cart(self):
        self.driver.find_element(*self.shopping_cart).click()