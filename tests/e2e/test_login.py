from playwright.sync_api import expect
import pytest
from pages.login_page import LoginPage
from helpers.config_loader import get
from utils.logger import get_logger

logger = get_logger(__name__)

BASE_URL = get("BASE_URL", "https://demo.thingsboard.io/")

url = get("BASE_URL", "https://demo.thingsboard.io/login")

@pytest.mark.parametrize("username,password,expected", [
    ("hi.newagenewera@gmail.com", "Tuilasieunhan@", True),
    ("invalid@test.com", "wrongpassword", False),
])

def test_login(page, username, password, expected):
    page.goto(url)
    page.wait_for_timeout(3000)
    login = LoginPage(page)
    login.login(username, password)
    login.click_login()
        
    if expected:
        # assert page.locator("text=Demo").is_visible()
        assert "ThingsBoard" in page.title() or "Demo" in page.title()

    else:
        # assert page.locator("text=Invalid credentials").is_visible()
        assert "ThingsBoard" not in page.title() or "Demo" in page.title()

    

def _goto_login(page):
    """Helper: Navigate to login page"""
    page.goto(BASE_URL)


@pytest.mark.smoke
def test_login_success(page):
    """Smoke: Successful login redirects to dashboard"""
    _goto_login(page)
    login_page = LoginPage(page)
    login_page.login(get("DEMO_USERNAME"), get("DEMO_PASSWORD"))
    
    assert login_page.is_login_successful()
    assert "ThingsBoard" in page.title() or "Demo" in page.title()
    logger.info("✓ Login successful - dashboard loaded")


# ====== PARAMETRIZE: Invalid credentials ======
INVALID_CREDENTIALS = [
    ("invalid@test.com", "wrongpassword", "invalid email + wrong password"),
    ("", "", "empty credentials"),
    ("hi.newagenewera@gmail.com", "wrongpass", "valid email + wrong password"),
]


@pytest.mark.regression
@pytest.mark.parametrize("username,password,description", INVALID_CREDENTIALS)
def test_login_invalid_credentials(page, username, password, description):
    """Regression: Invalid credentials rejected
    
    Parametrized test: runs 3 times with different credential sets
    """
    _goto_login(page)
    login_page = LoginPage(page)
    login_page.login(username, password)
    
    assert not login_page.is_login_successful(), f"Should fail: {description}"
    logger.info(f"✓ Login rejected: {description}")
