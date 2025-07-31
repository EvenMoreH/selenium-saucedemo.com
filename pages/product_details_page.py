from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver   # import to have intellisense inside methods
from selenium.common.exceptions import NoSuchElementException

class ProductDetails:
    """
    Represents the product details page on the website.

    Attributes:
        driver (WebDriver): The Selenium WebDriver instance.
    """
    # Locators:
    PRODUCT_DETAILS_NAME = (By.CLASS_NAME, "inventory_details_name")

    def __init__(self, driver: WebDriver):
        """
        Initializes the ProductDetails class with a WebDriver instance.

        Args:
            driver (WebDriver): The WebDriver instance to be used for interactions.
        """
        self.driver = driver

    def capture_product_name(self):
        """
        Captures and returns normalized product name from the details page.

        Returns:
            str: The normalized product name.
        """
        product_name = self.driver.find_element(*self.PRODUCT_DETAILS_NAME).text
        return product_name.lower().replace(" ", "-")