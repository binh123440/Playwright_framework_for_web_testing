from pages.login_page import LoginPage
from helpers.config_loader import get
import pytest

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

    

