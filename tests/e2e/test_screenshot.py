from pages.login_page import LoginPage
import pytest
from helpers.config_loader import get

def test_flai_and_capture123(page):
    url = get("BASE_URL", "https://playwright.dev/")
    page.goto(url)
    login = LoginPage(page)
    assert "Playwright" in page.title()
