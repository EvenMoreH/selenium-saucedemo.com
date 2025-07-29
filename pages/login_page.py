from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver   # import to have intellisense inside methods
from selenium.common.exceptions import NoSuchElementException


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

    def __init__(self, driver: WebDriver):
        """
        Initialize the LoginPage object.

        :param driver: The Selenium WebDriver instance used for interacting with the web page.
        """
        self.driver = driver

    def login(self, username, password):
        """
        Enter the provided username and password into the respective fields and click the login button.

        :param username: The username to be entered.
        :param password: The password to be entered.
        """
        self.driver.find_element(*self.USERNAME_INPUT).clear()
        self.driver.find_element(*self.USERNAME_INPUT).send_keys(username)
        self.driver.find_element(*self.PASSWORD_INPUT).clear()
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        self.driver.find_element(*self.LOGIN_BUTTON).click()

    def get_login_error_message(self):
        """
        Retrieve the text of any login error message displayed on the page.

        :return: The error message text if an error is present, otherwise an empty string.
        """
        try:
            return self.driver.find_element(*self.LOGIN_ERROR_MESSAGE).text
        except NoSuchElementException:
            return ""
