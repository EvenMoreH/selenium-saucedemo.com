from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.remote.webdriver import WebDriver   # import to have intellisense inside methods
from selenium.common.exceptions import NoSuchElementException

class ProductsPage:
    """
    Represents the products page of the website.

    This class provides methods for interacting with elements on the products page,
    such as adding and removing items from the cart, sorting products, and capturing
    product details like names and prices for sorting purposes.
    """
    # Locators:
    SHOPPING_CART_BTN = (By.CLASS_NAME, "shopping_cart_link")
    SHOPPING_CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    SORT_FUNNEL_BTN = (By.CLASS_NAME, "product_sort_container")
    PRODUCT_ITEM = (By.CLASS_NAME, "inventory_item")
    PRODUCT_NAME_ELEMENTS = (By.CLASS_NAME, "inventory_item_name")
    PRODUCT_PRICE_ELEMENTS = (By.CLASS_NAME, "inventory_item_price")
    # keep it resilient that is why partial link text if change to 'Visit our LinkedIn' would be made
    LINKEDIN_LINK = (By.PARTIAL_LINK_TEXT, "LinkedIn")

    def __init__(self, driver: WebDriver):
        """
        Initializes the ProductsPage object.

        :param driver: Selenium WebDriver instance
        """
        self.driver = driver

    def open_cart(self):
        """
        Clicks on the shopping cart button to open the cart.
        """
        self.driver.find_element(*self.SHOPPING_CART_BTN).click()

    def cart_badge_count(self):
        """
        Returns the number of items in the shopping cart badge.

        :return: Number of items in the cart, or 0 if the badge is not found
        """
        try:
            # needs to be dynamic to fetch fresh DOM each increment
            badge = self.driver.find_element(*self.SHOPPING_CART_BADGE)
            return int(badge.text)
        except NoSuchElementException:
            return 0

    # helper method to dynamically get the locators
    def _add_to_cart_locator(self, product_id: str):
        """
        Returns the locator for the 'Add to Cart' button of a specific product.

        :param product_id: Unique identifier for the product
        :return: Tuple containing By and value for locating the element
        """
        return (By.ID, f"add-to-cart-{product_id}")

    # helper method to dynamically get the locators
    def _remove_from_cart_locator(self, product_id: str):
        """
        Returns the locator for the 'Remove' button of a specific product.

        :param product_id: Unique identifier for the product
        :return: Tuple containing By and value for locating the element
        """
        return (By.ID, f"remove-{product_id}")

    def add_to_cart(self, product_id: str):
        """
        Adds a specific product to the shopping cart.

        :param product_id: Unique identifier for the product to be added
        :return: True if successful, False if the product is not found
        """
        try:
            # dynamic locator defined in method to not repeat it in __innit__
            self.driver.find_element(*self._add_to_cart_locator(product_id)).click()
        except NoSuchElementException:
            return False

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

    def is_add_to_cart_button_visible(self, product_id: str):
        """
        Checks if the 'Add to Cart' button for a specific product is visible.

        :param product_id: Unique identifier for the product
        :return: True if the button is visible, False otherwise
        """
        try:
            return self.driver.find_element(*self._add_to_cart_locator(product_id)).is_displayed()
        except NoSuchElementException:
            return False

    # helper method to open filter menu
    def _open_filter(self):
        """
        Returns the sort funnel dropdown element.

        :return: Web Element representing the sort funnel button
        """
        return self.driver.find_element(*self.SORT_FUNNEL_BTN)

    def sort_za(self):
        """
        Sorts products by name in descending order (Z to A).
        """
        select = Select(self._open_filter())
        select.select_by_value("za")

    def sort_az(self):
        """
        Sorts products by name in ascending order (A to Z).
        """
        select = Select(self._open_filter())
        select.select_by_value("az")

    def sort_high_low(self):
        """
        Sorts products by price in descending order (High to Low).
        """
        select = Select(self._open_filter())
        select.select_by_value("hilo")

    def sort_low_high(self):
        """
        Sorts products by price in ascending order (Low to High).
        """
        select = Select(self._open_filter())
        select.select_by_value("lohi")

    def capture_all_products_name(self):
        """
        Captures and returns the names of all products on the page.

        :return: List of product names
        """
        products_order = self.driver.find_elements(*self.PRODUCT_NAME_ELEMENTS)
        current_products_order = []
        current_products_order = [product.text.lower().replace(" ", "-") for product in products_order]

        print(current_products_order)
        return current_products_order

    def capture_all_products_price(self):
        """
        Captures and returns the prices of all products on the page.

        :return: List of product prices as floats
        """
        products_order = self.driver.find_elements(*self.PRODUCT_PRICE_ELEMENTS)
        current_products_order = []
        current_products_order = [float(product.text.replace("$", "")) for product in products_order]

        print(current_products_order)
        return current_products_order

    def visit_linkedin(self):
        """
        Clicks on the LinkedIn link to navigate to the company's LinkedIn page.
        """
        self.driver.find_element(*self.LINKEDIN_LINK).click()

    def open_product_details(self, product_id):
        """
        Clicks on the product with the given ID.

        Args:
            product_id (str): The product ID to be opened.
        """
        products = self.driver.find_elements(*self.PRODUCT_NAME_ELEMENTS)

        for product in products:
            normalized_name = product.text.lower().replace(" ", "-")
            if normalized_name == product_id:
                product.click()
                return

    def get_product_item(self, product_id):
        """
        Retrieves a product item by its ID.

        :param product_id: The unique identifier of the product.
        :return: A tuple containing the product name and price.
        :raises ValueError: If the product with the specified ID is not found.
        """
        products = self.driver.find_elements(*self.PRODUCT_ITEM)

        for product in products:
            name = product.find_element(*self.PRODUCT_NAME_ELEMENTS).text.lower().replace(" ", "-")
            price = product.find_element(*self.PRODUCT_PRICE_ELEMENTS).text.replace("$", "")
            if name == product_id:
                return name, price
        raise ValueError(f"Product with ID '{product_id}' not found on the page.")