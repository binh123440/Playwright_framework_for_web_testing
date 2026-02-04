from .base_page import BasePage


class LoginPage(BasePage):
    
 # Selectors
    # USERNAME_INPUT = "#username-input"
    # PASSWORD_INPUT = "#password-input"
    # LOGIN_BTN = "button[type='submit']"
    # ERROR_MSG = "text=/Invalid|incorrect|failed|error/i"
    # LOGIN_FORM = "form, [role='form']"
    
    USERNAME = "//input[@id='username-input']"
    PASSWORD = "//input[@id='password-input']"
    # LOGIN_BTN = "button[class*='mat-mdc-button-touch-target']"
    LOGIN_BTN = "button[type='submit']"
    ERROR_MSG = "text=/Invalid|incorrect|failed|error/i"
    LOGIN_FORM = "form, [role='form']"

    def login(self, username: str, password: str):
        self.page.fill(self.USERNAME, username)
        self.page.wait_for_timeout(2000)
        self.page.fill(self.PASSWORD, password)
        self.page.wait_for_timeout(2000)
        # self.click_login()

    def click_login(self):
        self.page.click(self.LOGIN_BTN)
        
    def is_login_successful(self) -> bool:
        """Kiểm tra đăng nhập thành công (URL không chứa 'login')"""
        is_success = "login" not in self.get_current_url().lower()
        self.logger.info(f"Login successful: {is_success}")
        return is_success
    
    def is_login_form_visible(self, timeout: int = 5000) -> bool:
        """Kiểm tra form login có tồn tại"""
        return self.is_visible(self.LOGIN_FORM, timeout=timeout)

    def get_error_message(self, timeout: int = 3000) -> str:
        """Lấy thông báo lỗi nếu có"""
        try:
            error = self.page.locator(self.ERROR_MSG).first.text_content(timeout=timeout)
            self.logger.warning(f"Login error message: {error}")
            return error
        except Exception as e:
            self.logger.debug(f"No error message found: {e}")
            return ""
