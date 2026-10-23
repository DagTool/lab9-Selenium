import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


class BasePage:
    """Lớp BasePage định nghĩa các phương thức thao tác Web phổ biến sử dụng Explicit Wait."""

    def __init__(self, driver):
        self.driver = driver
        self.default_timeout = 10

    def open_url(self, url: str):
        """Mở đường dẫn URL trên trình duyệt."""
        self.driver.get(url)

    def find_element(self, locator: tuple, timeout: int = None):
        """Tìm 1 phần tử với explicit wait cho đến khi phần tử xuất hiện trong DOM."""
        timeout = timeout or self.default_timeout
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def find_visible_element(self, locator: tuple, timeout: int = None):
        """Tìm 1 phần tử và chờ đến khi hiển thị rõ ràng trên màn hình."""
        timeout = timeout or self.default_timeout
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def find_elements(self, locator: tuple, timeout: int = None):
        """Tìm danh sách tất cả các phần tử phù hợp locator."""
        timeout = timeout or self.default_timeout
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
        return self.driver.find_elements(*locator)

    def click(self, locator: tuple, timeout: int = None):
        """Chờ phần tử có thể click được và tiến hành click."""
        timeout = timeout or self.default_timeout
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()

    def enter_text(self, locator: tuple, text: str, timeout: int = None, clear_first: bool = True):
        """Chờ phần tử hiển thị, xóa nội dung cũ (nếu có) và nhập văn bản mới."""
        element = self.find_visible_element(locator, timeout)
        if clear_first:
            element.clear()
        element.send_keys(text)

    def get_text(self, locator: tuple, timeout: int = None) -> str:
        """Lấy chuỗi văn bản của phần tử hiển thị."""
        return self.find_visible_element(locator, timeout).text.strip()

    def is_visible(self, locator: tuple, timeout: int = 4) -> bool:
        """Kiểm tra phần tử có đang hiển thị hay không (trả về True/False, không ném exception làm fail test)."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except Exception:
            return False

    def select_by_value(self, locator: tuple, value: str, timeout: int = None):
        """Chọn giá trị trong thẻ <select> theo value."""
        element = self.find_visible_element(locator, timeout)
        select = Select(element)
        select.select_by_value(value)

    def select_by_visible_text(self, locator: tuple, text: str, timeout: int = None):
        """Chọn giá trị trong thẻ <select> theo text hiển thị."""
        element = self.find_visible_element(locator, timeout)
        select = Select(element)
        select.select_by_visible_text(text)

    def wait_for_url(self, url_fragment: str, timeout: int = None) -> bool:
        """Chờ cho đến khi URL hiện tại chứa đoạn ký tự chỉ định."""
        timeout = timeout or self.default_timeout
        return WebDriverWait(self.driver, timeout).until(
            EC.url_contains(url_fragment)
        )

    def get_current_url(self) -> str:
        """Lấy URL hiện tại của trang."""
        return self.driver.current_url

    def get_page_title(self) -> str:
        """Lấy tiêu đề (title) của trang."""
        return self.driver.title

    def save_screenshot(self, filepath: str):
        """Chụp ảnh màn hình lưu vào thư mục chỉ định."""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        self.driver.save_screenshot(filepath)
