from pages.login_page import LoginPage
import pytest

def test_flai_and_capture123(page):
    # go to a blank page and intentionally fail to trigger screenshot capture
    page.goto("about:blank")
    login = LoginPage(page)
    with pytest.raises(Exception):
        page.click("#this_element_does_not_exist")
    pytest.fail("intentional failure to test screenshot capture")
