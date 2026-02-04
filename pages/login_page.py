from .base_page import BasePage


class LoginPage(BasePage):
    def fill_username(self, username: str):
        """Fill username using accessible role locator"""
        self.page.get_by_role("textbox", name="Username (email)").fill(username)
    
    def fill_password(self, password: str):
        """Fill password field"""
        self.page.get_by_role("textbox", name="Password").fill(password)
    
    def click_login_button(self):
        """Click login button using role"""
        self.page.get_by_role("button", name="Sign in").click()
    
    def login(self, username: str, password: str):
        """Complete login flow"""
        self.fill_username(username)
        self.fill_password(password)
        self.click_login_button()
