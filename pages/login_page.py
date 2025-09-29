from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver   # import to have intellisense inside methods
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    """
    A class representing the login page of a web application.

    This class provides methods to interact with the login form, including entering credentials and logging in.
    """
    # Locators
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    LOGIN_ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")

    # Page Identifiers
    LOGIN_FORM = (By.CLASS_NAME, "login_wrapper")
    PRODUCTS_PAGE = (By.ID, "inventory_container")

    def __init__(self, driver: WebDriver, timeout: int = 10):
        """
        Initialize the LoginPage object.

        :param driver: The Selenium WebDriver instance used for interacting with the web page.
        """
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(self.driver, self.timeout)


    def wait_for_login_page_to_load(self):
        """
        Wait for the login page to be fully loaded and ready for interaction.

        :return: Self for method chaining
        """
        self.wait.until(EC.visibility_of_element_located(self.LOGIN_FORM))
        return self


    def login(self, username, password):
        """
        Enter the provided username and password into the respective fields and click the login button.

        :param username: The username to be entered.
        :param password: The password to be entered.
        """
        username_field = self.wait.until(EC.element_to_be_clickable(self.USERNAME_INPUT))
        password_field = self.wait.until(EC.element_to_be_clickable(self.PASSWORD_INPUT))
        login_button = self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))

        username_field.clear()
        username_field.send_keys(username)

        password_field.clear()
        password_field.send_keys(password)

        login_button.click()

    def get_login_error_message(self):
        """
        Retrieve the text of any login error message displayed on the page.

        :return: The error message text if an error is present, otherwise an empty string.
        """
        try:
            error_element = self.wait.until(EC.visibility_of_element_located(self.LOGIN_ERROR_MESSAGE))
            return error_element.text
        except TimeoutException:
            return ""


    # def was_login_successful(self):
    #     """
    #     Check if login was successful by verifying redirect to inventory page.

    #     :return: True if login was successful, False otherwise
    #     """
    #     try:
    #         self.wait.until(EC.presence_of_element_located(self.PRODUCTS_PAGE))
    #         return True
    #     except TimeoutException:
    #         return False