from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CartPage(BasePage):
    """Page Object cho màn hình Giỏ hàng (Cart Page)."""

    PAGE_TITLE = (By.CSS_SELECTOR, "span.title")
    CART_ITEMS = (By.CSS_SELECTOR, "div.cart_item")
    ITEM_NAMES = (By.CSS_SELECTOR, "div.inventory_item_name")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")

    def get_title_text(self) -> str:
        """Lấy tiêu đề trang (ví dụ: 'Your Cart')."""
        return self.get_text(self.PAGE_TITLE)

    def get_cart_item_names(self) -> list[str]:
        """Lấy danh sách tên các sản phẩm trong giỏ hàng."""
        if not self.is_visible(self.CART_ITEMS, timeout=3):
            return []
        elements = self.find_elements(self.ITEM_NAMES)
        return [e.text.strip() for e in elements]

    def click_checkout(self):
        """Click nút Checkout để chuyển sang bước thanh toán."""
        self.click(self.CHECKOUT_BUTTON)
