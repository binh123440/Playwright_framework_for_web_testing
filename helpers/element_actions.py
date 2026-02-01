from playwright.sync_api import Page


def click(page: Page, selector: str):
    page.click(selector)


def type_text(page: Page, selector: str, text: str):
    page.fill(selector, text)


def get_text(page: Page, selector: str):
    return page.text_content(selector)
