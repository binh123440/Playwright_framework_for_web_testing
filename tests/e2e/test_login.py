import pytest
from pages.login_page import LoginPage
from helpers.config_loader import get
from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.smoke
def test_login_success(page):
    """Smoke test: successful login with valid credentials"""
    page.goto(get("BASE_URL", "https://demo.thingsboard.io/"))
    login_page = LoginPage(page)
    login_page.login(get("DEMO_USERNAME"), get("DEMO_PASSWORD"))
    assert login_page.is_login_successful()
    logger.info("✓ Login successful - redirected to dashboard")
    # Check page has title
    assert page.title() != ""
    # Check it's ThingsBoard
    assert "ThingsBoard" in page.title() or "Demo" in page.title()

