from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class InventoryPage(BasePage):
    """Page Object cho màn hình Danh sách sản phẩm (Inventory/Products Page)."""

    PAGE_TITLE = (By.CSS_SELECTOR, "span.title")
    SORT_SELECT = (By.CSS_SELECTOR, "[data-test='product-sort-container']")
    ITEM_PRICES = (By.CSS_SELECTOR, "div.inventory_item_price")
    ITEM_NAMES = (By.CSS_SELECTOR, "div.inventory_item_name")
    ADD_BACKPACK_BTN = (By.ID, "add-to-cart-sauce-labs-backpack")
    REMOVE_BACKPACK_BTN = (By.ID, "remove-sauce-labs-backpack")
    CART_BADGE = (By.CSS_SELECTOR, "span.shopping_cart_badge")
    CART_LINK = (By.CSS_SELECTOR, "a.shopping_cart_link")
    BURGER_MENU_BTN = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")

    def get_title_text(self) -> str:
        """Lấy tiêu đề trang (ví dụ: 'Products')."""
        return self.get_text(self.PAGE_TITLE)

    def sort_products_by(self, value: str):
        """
        Sắp xếp danh sách sản phẩm.
        Các giá trị hợp lệ:
        - 'az' : Name (A to Z)
        - 'za' : Name (Z to A)
        - 'lohi': Price (low to high)
        - 'hilo': Price (high to low)
        """
        self.select_by_value(self.SORT_SELECT, value)

    def get_all_product_prices(self) -> list[float]:
        """Lấy danh sách tất cả giá tiền của các sản phẩm trên trang dạng float."""
        price_elements = self.find_elements(self.ITEM_PRICES)
        prices = []
        for elem in price_elements:
            # Format text: "$29.99" -> float(29.99)
            cleaned_price = elem.text.replace("$", "").strip()
            prices.append(float(cleaned_price))
        return prices

    def get_all_product_names(self) -> list[str]:
        """Lấy danh sách tên tất cả sản phẩm."""
        name_elements = self.find_elements(self.ITEM_NAMES)
        return [elem.text.strip() for elem in name_elements]

    def add_backpack_to_cart(self):
        """Thêm sản phẩm Sauce Labs Backpack vào giỏ hàng."""
        self.click(self.ADD_BACKPACK_BTN)

    def remove_backpack_from_cart(self):
        """Xóa sản phẩm Sauce Labs Backpack khỏi giỏ hàng."""
        self.click(self.REMOVE_BACKPACK_BTN)

    def is_backpack_remove_button_displayed(self) -> bool:
        """Kiểm tra nút Remove của Backpack có hiển thị không."""
        return self.is_visible(self.REMOVE_BACKPACK_BTN)

    def get_cart_badge_count(self) -> str:
        """Lấy số lượng hiển thị trên icon giỏ hàng."""
        if self.is_visible(self.CART_BADGE, timeout=2):
            return self.get_text(self.CART_BADGE)
        return "0"

    def is_cart_badge_displayed(self) -> bool:
        """Kiểm tra badge số lượng giỏ hàng có hiển thị không."""
        return self.is_visible(self.CART_BADGE, timeout=2)

    def go_to_cart(self):
        """Chuyển đến trang Giỏ hàng."""
        self.click(self.CART_LINK)

    def logout(self):
        """Mở menu điều hướng bên trái và nhấn Đăng xuất (Logout)."""
        self.click(self.BURGER_MENU_BTN)
        self.click(self.LOGOUT_LINK)
