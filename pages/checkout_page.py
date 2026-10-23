from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    """Page Object cho quy trình Thanh toán (Checkout Steps & Complete)."""

    # Step One Locators
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    CANCEL_BUTTON = (By.ID, "cancel")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    # Step Two Locators
    SUMMARY_SUBTOTAL = (By.CSS_SELECTOR, "div.summary_subtotal_label")
    SUMMARY_TAX = (By.CSS_SELECTOR, "div.summary_tax_label")
    SUMMARY_TOTAL = (By.CSS_SELECTOR, "div.summary_total_label")
    FINISH_BUTTON = (By.ID, "finish")

    # Step Complete Locators
    COMPLETE_HEADER = (By.CSS_SELECTOR, "h2.complete-header")
    COMPLETE_TEXT = (By.CSS_SELECTOR, "div.complete-text")
    BACK_HOME_BUTTON = (By.ID, "back-to-products")

    def fill_checkout_info(self, first_name: str, last_name: str, postal_code: str):
        """Điền thông tin khách hàng ở bước 1."""
        self.enter_text(self.FIRST_NAME_INPUT, first_name)
        self.enter_text(self.LAST_NAME_INPUT, last_name)
        self.enter_text(self.POSTAL_CODE_INPUT, postal_code)
        self.click(self.CONTINUE_BUTTON)

    def get_error_message(self) -> str:
        """Lấy thông báo lỗi nếu nhập thiếu thông tin checkout."""
        return self.get_text(self.ERROR_MESSAGE)

    def get_summary_total_text(self) -> str:
        """Lấy dòng tổng tiền đơn hàng (ví dụ: 'Total: $32.39')."""
        return self.get_text(self.SUMMARY_TOTAL)

    def click_finish(self):
        """Click nút hoàn tất đơn hàng."""
        self.click(self.FINISH_BUTTON)

    def get_complete_header(self) -> str:
        """Lấy thông báo chúc mừng đặt hàng thành công."""
        return self.get_text(self.COMPLETE_HEADER)

    def is_back_home_button_displayed(self) -> bool:
        """Kiểm tra nút Back Home có hiển thị hay không."""
        return self.is_visible(self.BACK_HOME_BUTTON)
