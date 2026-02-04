def test_open_google(page):
    page.goto("https://www.google.com")
    page.wait_for_timeout(3000)
    assert "Google" in page.title()