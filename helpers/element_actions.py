from playwright.sync_api import Page
from utils.logger import get_logger

logger = get_logger(__name__)


def click(page: Page, selector: str, timeout: int = 5000) -> None:
    """Click on element with error handling"""
    try:
        page.click(selector, timeout=timeout)
        logger.debug(f"Clicked on selector: {selector}")
    except Exception as e:
        logger.error(f"Failed to click on {selector}: {e}")
        raise


def fill(page: Page, selector: str, text: str, timeout: int = 5000) -> None:
    """Fill input with error handling"""
    try:
        page.fill(selector, text, timeout=timeout)
        logger.debug(f"Filled '{selector}' with text")
    except Exception as e:
        logger.error(f"Failed to fill {selector}: {e}")
        raise


def get_text(page: Page, selector: str, timeout: int = 5000) -> str:
    """Get text from element"""
    try:
        text = page.text_content(selector, timeout=timeout)
        logger.debug(f"Got text from {selector}: {text}")
        return text
    except Exception as e:
        logger.error(f"Failed to get text from {selector}: {e}")
        raise


def is_visible(page: Page, selector: str, timeout: int = 5000) -> bool:
    """Check if element is visible"""
    try:
        return page.locator(selector).is_visible(timeout=timeout)
    except Exception as e:
        logger.debug(f"Element {selector} not visible: {e}")
        return False


def wait_for_element(page: Page, selector: str, timeout: int = 5000) -> None:
    """Wait for element to be visible"""
    try:
        page.wait_for_selector(selector, timeout=timeout)
        logger.debug(f"Element {selector} is visible")
    except Exception as e:
        logger.error(f"Timeout waiting for {selector}: {e}")
        raise
