from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page Object cho màn hình Đăng nhập (Login Page) của SauceDemo."""

    URL = "https://www.saucedemo.com/"

    # Locators
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    def open(self):
        """Mở trang đăng nhập."""
        self.open_url(self.URL)
        return self

    def enter_username(self, username: str):
        """Nhập tên đăng nhập."""
        self.enter_text(self.USERNAME_INPUT, username)
        return self

    def enter_password(self, password: str):
        """Nhập mật khẩu."""
        self.enter_text(self.PASSWORD_INPUT, password)
        return self

    def click_login(self):
        """Click nút đăng nhập."""
        self.click(self.LOGIN_BUTTON)

    def login(self, username: str, password: str):
        """Thực hiện toàn bộ quá trình đăng nhập."""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def get_error_message(self) -> str:
        """Lấy thông báo lỗi khi đăng nhập không thành công."""
        return self.get_text(self.ERROR_MESSAGE)

    def is_login_button_displayed(self) -> bool:
        """Kiểm tra nút login có đang hiển thị hay không (dùng khi kiểm tra đã về trang login sau logout)."""
        return self.is_visible(self.LOGIN_BUTTON)
