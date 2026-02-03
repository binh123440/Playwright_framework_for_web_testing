from .base_page import BasePage


class LoginPage(BasePage):
    # selectors mapped from the Appium project's LoginPage
    PHONE = "input#PhoneNumberInput, [resource-id='PhoneNumberInput']"
    PASSWORD = "input#PasswordInput, [resource-id='PasswordInput']"
    LOGIN_BTN = "text='Log in', [content-desc='Log in']"

    def login(self, phone: str, password: str):
        self.page.fill(self.PHONE, phone)
        self.page.wait_for_timeout(2000)
        self.page.fill(self.PASSWORD, password)
        self.page.wait_for_timeout(2000)

    def click_login(self):
        self.page.click(self.LOGIN_BTN)