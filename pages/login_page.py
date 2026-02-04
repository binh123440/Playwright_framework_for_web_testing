from .base_page import BasePage


class LoginPage(BasePage):
    
 # Selectors
    USERNAME_INPUT = "#username-input"
    PASSWORD_INPUT = "#password-input"
    LOGIN_BTN = "button[type='submit']"
    ERROR_MSG = "text=/Invalid|incorrect|failed|error/i"
    LOGIN_FORM = "form, [role='form']"
    
    USERNAME = "//input[@id='username-input']"
    PASSWORD = "//input[@id='password-input']"
    # LOGIN_BTN = "//button[@type='submit']"
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
        
    def enter_username(self, username: str, timeout: int = 5000) -> None:
        """Nhập username"""
        self.logger.info(f"Entering username")
        self.page.fill(self.USERNAME_INPUT, username, timeout=timeout)

    def enter_password(self, password: str, timeout: int = 5000) -> None:
        """Nhập password"""
        self.logger.info(f"Entering password")
        self.page.fill(self.PASSWORD_INPUT, password, timeout=timeout)

    def click_login(self, timeout: int = 10000) -> None:
        """Click nút Login"""
        self.logger.info(f"Clicking login button")
        self.page.click(self.LOGIN_BTN, timeout=timeout)
        # Wait for navigation
        self.page.wait_for_load_state("networkidle", timeout=timeout)

    def login(self, username: str, password: str, timeout: int = 10000) -> None:
        """Đăng nhập với username và password"""
        self.logger.info(f"Performing login with username: {username}")
        self.wait_for(self.LOGIN_FORM, timeout=timeout)
        self.enter_username(username, timeout=timeout)
        self.enter_password(password, timeout=timeout)
        self.click_login(timeout=timeout)

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
