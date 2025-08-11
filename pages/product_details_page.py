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
    PRODUCT_ITEM = (By.CLASS_NAME, "inventory_item_container")
    PRODUCT_DETAILS_NAME = (By.CLASS_NAME, "inventory_details_name")
    PRODUCT_DETAILS_PRICE = (By.CLASS_NAME, "inventory_details_price")
    BACK_TO_PRODUCTS_BTN = (By.ID, "back-to-products")
    ADD_TO_CART_BTN = (By.ID, "add-to-cart")
    REMOVE_BTN = (By.ID, "remove")

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

    def click_back_to_products(self):
        """
        Clicks on the back to products button.
        """
        self.driver.find_element(*self.BACK_TO_PRODUCTS_BTN).click()

    def add_to_cart(self):
        """
        Adds an item to the shopping cart.
        """
        self.driver.find_element(*self.ADD_TO_CART_BTN).click()

    def is_in_cart(self):
        """
        Checks if the item is present in the cart based on Remove button availability.

        Returns:
            bool: True if the item is in the cart, False otherwise.
        """
        try:
            return self.driver.find_element(*self.REMOVE_BTN).is_displayed()
        except NoSuchElementException:
            return False

    def remove_from_cart(self):
        """
        Removes an item from the shopping cart.

        Returns:
            bool: True if the removal is successful, False if the item is not found.
        """
        try:
            self.driver.find_element(*self.REMOVE_BTN).click()
        except NoSuchElementException:
            return False

    def get_product_item(self, product_id):
        """
        Retrieves a product item by its ID.

        :param product_id: The unique identifier of the product.
        :return: A tuple containing the product name and price.
        :raises ValueError: If the product with the specified ID is not found.
        """
        products = self.driver.find_elements(*self.PRODUCT_ITEM)

        for product in products:
            name = product.find_element(*self.PRODUCT_DETAILS_NAME).text.lower().replace(" ", "-")
            price = product.find_element(*self.PRODUCT_DETAILS_PRICE).text.replace("$", "")
            if name == product_id:
                return name, price
        raise ValueError(f"Product with ID '{product_id}' not found on the page.")