import pytest
from pages.login_page import LoginPage
from helpers.config_loader import get
from utils.logger import get_logger

logger = get_logger(__name__)

BASE_URL = get("BASE_URL", "https://demo.thingsboard.io/")


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