from dotenv import load_dotenv
import os

load_dotenv()

TEST_USER = os.getenv("TEST_USER")
TEST_PASS = os.getenv("TEST_PASS")

BASE_URL = "https://www.saucedemo.com/"
DEFAULT_TIMEOUT = 10