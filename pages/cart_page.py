from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver   # import to have intellisense inside methods
from selenium.common.exceptions import NoSuchElementException

class Cart:
    """
    Represents the shopping cart page of an e-commerce website.

    This class provides methods for interacting with elements on the cart page,
    such as removing items from the cart and checking out.
    """
    # Locators:
    CONTINUE_SHOPPING_BTN = (By.ID, "continue-shopping")
    CHECKOUT_BTN = (By.ID, "checkout")

    def __init__(self, driver: WebDriver):
        """
        Initializes the Cart object.

        :param driver: Selenium WebDriver instance
        """
        self.driver = driver

    def return_to_products_page(self):
        """
        Clicks on the 'Continue Shopping' button to navigate back to the products page.
        """
        self.driver.find_element(*self.CONTINUE_SHOPPING_BTN).click()

    # helper method to dynamically get the locators
    def _remove_from_cart_locator(self, product_id: str):
        """
        Returns the locator for the 'Remove' button of a specific product.

        :param product_id: Unique identifier for the product
        :return: Tuple containing By and value for locating the element
        """
        return (By.ID, f"remove-{product_id}")

    def is_in_cart(self, product_id: str):
        """
        Checks if a specific product is already in the shopping cart.

        :param product_id: Unique identifier for the product
        :return: True if the product is in the cart, False otherwise
        """
        try:
            # returning if remove button is displayed
            return self.driver.find_element(*self._remove_from_cart_locator(product_id)).is_displayed()
        except NoSuchElementException:
            return False

    def remove_from_cart(self, product_id: str):
        """
        Removes a specific product from the shopping cart.

        :param product_id: Unique identifier for the product to be removed
        :return: True if successful, False if the product is not found
        """
        try:
            self.driver.find_element(*self._remove_from_cart_locator(product_id)).click()
        except NoSuchElementException:
            return False