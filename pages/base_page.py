class BasePage:
    """Common page utilities to be extended by page objects."""
    def __init__(self, page):
        self.page = page

    def goto(self, url: str):
        self.page.goto(url)

    def wait_for(self, selector: str, timeout: int = 5000):
        return self.page.wait_for_selector(selector, timeout=timeout)
