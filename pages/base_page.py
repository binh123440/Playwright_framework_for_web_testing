from utils.logger import get_logger

logger = get_logger(__name__)

class BasePage:
    """Common page utilities to be extended by page objects."""
    def __init__(self, page):
        self.page = page

    def goto(self, url: str):
        self.page.goto(url)

    def wait_for(self, selector: str, timeout: int = 5000):
        return self.page.wait_for_selector(selector, timeout=timeout)
    
    def is_visible(self, selector: str, timeout: int = 5000) -> bool:
        """Check if element is visible"""
        try:
            self.page.locator(selector).is_visible(timeout=timeout)
            return True
        except:
            return False
    
    def get_current_url(self) -> str:
        """Get current page URL"""
        return self.page.url
    
    def get_title(self) -> str:
        """Get page title"""
        return self.page.title()
