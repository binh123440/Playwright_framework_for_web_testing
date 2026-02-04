from utils.logger import get_logger

logger = get_logger(__name__)

class BasePage:
    """Common page utilities to be extended by page objects."""
    
    def __init__(self, page):
        self.page = page
        self.logger = logger

    def goto(self, url: str, timeout: int = 30000) -> None:
        """Navigate to URL"""
        self.logger.info(f"Navigating to: {url}")
        self.page.goto(url, timeout=timeout)
        self.page.wait_for_load_state("networkidle", timeout=timeout)

    def wait_for(self, selector: str, timeout: int = 5000):
        """Wait for element to be visible"""
        self.logger.debug(f"Waiting for selector: {selector}")
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
