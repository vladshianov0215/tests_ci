import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.dev-cinescope.coconutqa.ru"
BASE_UI_URL = "https://dev-cinescope.coconutqa.ru"
BASE_AUTH_URL = "https://auth.dev-cinescope.coconutqa.ru"

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

MOVIES_ENDPOINT = "/movies"
CREATE_MOVIE_ENDPOINT = "/movies"
MOVIE_BY_ID_ENDPOINT = "/movies/{movie_id}"

LOGIN_ENDPOINT = "/login"
REGISTER_ENDPOINT = "/register"
LOGOUT_ENDPOINT = "/logout"
REFRESH_ENDPOINT = "/refresh-tokens"

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

NON_EXISTENT_ID = 999999999 

CARD_NUMBER = "4242424242424242"
HOLDER_NAME = "Test User"
EXP_MONTH = "Декабрь"
EXP_YEAR = "2025"
CVC = "123" 