from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.remote.webdriver import WebDriver   # import to have intellisense inside methods
from selenium.common.exceptions import NoSuchElementException

class ProductsPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.shopping_cart = (By.CLASS_NAME, "shopping_cart_link")
        self.sort_funnel = (By.CLASS_NAME, "product_sort_container")

    def open_cart(self):
        self.driver.find_element(*self.shopping_cart).click()

    def cart_badge_count(self):
        try:
            # needs to be dynamic to fetch fresh DOM each increment
            badge = self.driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
            return int(badge.text)
        except NoSuchElementException:
            return 0

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

    # helper method to open filter menu
    def _open_filter(self):
        return self.driver.find_element(*self.sort_funnel)

    def sort_za(self):
        select = Select(self._open_filter())
        select.select_by_value("za")

    def sort_az(self):
        select = Select(self._open_filter())
        select.select_by_value("az")

    def sort_high_low(self):
        select = Select(self._open_filter())
        select.select_by_value("hilo")

    def sort_low_high(self):
        select = Select(self._open_filter())
        select.select_by_value("lohi")

    def capture_all_products_name(self):
        products_order = self.driver.find_elements(By.CLASS_NAME, "inventory_item_name")
        current_products_order = []
        for product in products_order:
            current_products_order.append(product.text.lower().replace(" ", "-"))
        print(current_products_order)
        return current_products_order

    def capture_all_products_price(self):
        products_order = self.driver.find_elements(By.CLASS_NAME, "inventory_item_price")
        current_products_order = []
        for product in products_order:
            product = float(product.text.replace("$", ""))
            current_products_order.append(product)

        print(current_products_order)
        return current_products_order