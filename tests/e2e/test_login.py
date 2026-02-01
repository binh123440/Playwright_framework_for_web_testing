from pages.login_page import LoginPage
from helpers.config_loader import get


def test_open_home_and_title(page):
    url = get("BASE_URL", "https://playwright.dev/")
    page.goto(url)
    login = LoginPage(page)
    assert "Playwright" in page.title()
