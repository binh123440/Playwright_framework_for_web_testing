from playwright.sync_api import expect
from pages.login_page import LoginPage
from helpers.config_loader import get


def test_open_home_and_title(page):
    url = get("BASE_URL", "https://demo.thingsboard.io/login")
    page.goto(url)

    login = LoginPage(page)

    login.login("hi.newagenewera@gmail.com", "Tuilasieunhan@")

    # Kiểm tra URL đã chuyển sang trang /home
    expect(page).to_have_url("https://demo.thingsboard.io/home")