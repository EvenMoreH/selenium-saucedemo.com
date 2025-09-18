from dotenv import load_dotenv
import os

BASE_URL = "https://www.saucedemo.com/"
SOCIAL_MEDIA = "https://www.linkedin.com/company/sauce-labs/"
DEFAULT_TIMEOUT = 10

load_dotenv()

class TestUsers:
    standard: dict[str, str] = {
        "username": os.getenv("TEST_STANDARD_USER", ""),
        "password": os.getenv("TEST_STANDARD_PASS", ""),
    }
    incorrect: dict[str, str] = {
        "username": os.getenv("TEST_INCORRECT_USER", ""),
        "password": os.getenv("TEST_INCORRECT_PASS", ""),
    }
    locked: dict[str, str] = {
        "username": os.getenv("TEST_LOCKED_USER", ""),
        "password": os.getenv("TEST_LOCKED_PASS", ""),
    }
    problem: dict[str, str] = {
        "username": os.getenv("TEST_PROBLEM_USER", ""),
        "password": os.getenv("TEST_PROBLEM_PASS", ""),
    }
