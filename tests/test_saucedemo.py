import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


class TestSauceDemo:
    """Bộ kiểm thử tự động cho hệ thống thương mại điện tử SauceDemo."""

    def test_tc01_login_success(self, driver):
        """
        TC01: Kiểm tra đăng nhập thành công với thông tin tài khoản hợp lệ.
        - Dữ liệu: standard_user / secret_sauce
        - Kỳ vọng: Chuyển hướng đến inventory.html, hiển thị danh mục 'Products' và các sản phẩm.
        """
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("standard_user", "secret_sauce")

        inventory_page = InventoryPage(driver)
        # Chờ chuyển hướng trang
        inventory_page.wait_for_url("inventory.html")

        # Kiểm tra URL và tiêu đề trang
        assert "inventory.html" in inventory_page.get_current_url(), "URL không đúng sau khi đăng nhập thành công!"
        assert inventory_page.get_title_text() == "Products", "Tiêu đề trang sản phẩm không khớp!"
        
        # Kiểm tra có ít nhất 1 sản phẩm hiển thị trên màn hình
        products = inventory_page.get_all_product_names()
        assert len(products) > 0, "Không tìm thấy sản phẩm nào trong kho hàng!"
        print(f"\n[TC01 PASS] Đăng nhập thành công, tìm thấy {len(products)} sản phẩm.")

    def test_tc02_login_invalid_password(self, driver):
        """
        TC02: Kiểm tra đăng nhập thất bại khi nhập sai mật khẩu.
        - Dữ liệu: standard_user / wrong_password_123
        - Kỳ vọng: Hiển thị thông báo lỗi 'Epic sadface: Username and password do not match any user in this service'.
        """
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("standard_user", "wrong_password_123")

        # Kiểm tra thông báo lỗi
        expected_error_msg = "Epic sadface: Username and password do not match any user in this service"
        actual_error_msg = login_page.get_error_message()
        assert expected_error_msg in actual_error_msg, f"Thông báo lỗi hiển thị không đúng! Thực tế: {actual_error_msg}"
        print(f"\n[TC02 PASS] Bắt lỗi đăng nhập sai mật khẩu chính xác: '{actual_error_msg}'.")

    def test_tc03_sort_products_price_low_to_high(self, driver):
        """
        TC03: Kiểm tra tính năng lọc và sắp xếp sản phẩm theo giá tăng dần (Price: low to high).
        - Kỳ vọng: Danh sách giá sản phẩm hiển thị phải được sắp xếp theo thứ tự tăng dần.
        """
        # Bước 1: Đăng nhập
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("standard_user", "secret_sauce")

        inventory_page = InventoryPage(driver)
        inventory_page.wait_for_url("inventory.html")

        # Bước 2: Chọn sắp xếp giá từ thấp đến cao (lohi)
        inventory_page.sort_products_by("lohi")

        # Bước 3: Lấy danh sách giá tiền thực tế trên giao diện
        prices = inventory_page.get_all_product_prices()
        assert len(prices) > 0, "Không lấy được danh sách giá sản phẩm!"

        # Bước 4: So sánh với mảng đã sắp xếp tăng dần
        expected_sorted_prices = sorted(prices)
        assert prices == expected_sorted_prices, f"Thứ tự giá không tăng dần! Thực tế: {prices}"
        print(f"\n[TC03 PASS] Sắp xếp giá từ thấp đến cao thành công: {prices}")

    def test_tc04_add_and_remove_product_cart(self, driver):
        """
        TC04: Kiểm tra tính năng thêm sản phẩm vào giỏ hàng và xóa sản phẩm khỏi giỏ hàng.
        - Kỳ vọng:
          1. Khi bấm 'Add to cart', badge giỏ hàng hiển thị số '1' và nút đổi thành 'Remove'.
          2. Khi bấm 'Remove', badge giỏ hàng biến mất hoặc về '0'.
        """
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("standard_user", "secret_sauce")

        inventory_page = InventoryPage(driver)
        inventory_page.wait_for_url("inventory.html")

        # Thêm Sauce Labs Backpack vào giỏ
        inventory_page.add_backpack_to_cart()

        # Kiểm tra badge giỏ hàng cập nhật số 1
        assert inventory_page.get_cart_badge_count() == "1", "Badge giỏ hàng không cập nhật số 1 sau khi thêm!"
        assert inventory_page.is_backpack_remove_button_displayed(), "Nút chưa đổi sang trạng thái 'Remove'!"

        # Xóa sản phẩm khỏi giỏ hàng
        inventory_page.remove_backpack_from_cart()

        # Kiểm tra badge đã biến mất
        assert not inventory_page.is_cart_badge_displayed(), "Badge giỏ hàng vẫn còn sau khi xóa sản phẩm!"
        print("\n[TC04 PASS] Thêm và xóa sản phẩm vào giỏ hàng hoạt động chính xác.")

    def test_tc05_complete_checkout_journey(self, driver):
        """
        TC05: Kiểm tra toàn bộ quy trình đặt hàng thành công (End-to-End Checkout Flow).
        - Các bước: Thêm sản phẩm -> Mở giỏ hàng -> Checkout -> Nhập thông tin khách hàng -> Xem tổng tiền -> Finish.
        - Kỳ vọng: Hiển thị thông báo 'Thank you for your order!' và nút 'Back Home'.
        """
        # Bước 1: Đăng nhập
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("standard_user", "secret_sauce")

        # Bước 2: Thêm sản phẩm và mở giỏ hàng
        inventory_page = InventoryPage(driver)
        inventory_page.wait_for_url("inventory.html")
        inventory_page.add_backpack_to_cart()
        inventory_page.go_to_cart()

        # Bước 3: Kiểm tra giỏ hàng và nhấn Checkout
        cart_page = CartPage(driver)
        cart_page.wait_for_url("cart.html")
        items = cart_page.get_cart_item_names()
        assert "Sauce Labs Backpack" in items, "Sản phẩm không có trong giỏ hàng!"
        cart_page.click_checkout()

        # Bước 4: Nhập thông tin thanh toán (Step 1)
        checkout_page = CheckoutPage(driver)
        checkout_page.wait_for_url("checkout-step-one.html")
        checkout_page.fill_checkout_info("Nguyen", "Van A", "700000")

        # Bước 5: Xem trước đơn hàng (Step 2)
        checkout_page.wait_for_url("checkout-step-two.html")
        total_text = checkout_page.get_summary_total_text()
        assert "Total:" in total_text, f"Không tìm thấy thông tin tổng tiền! Thực tế: {total_text}"
        checkout_page.click_finish()

        # Bước 6: Kiểm tra màn hình hoàn tất đặt hàng
        checkout_page.wait_for_url("checkout-complete.html")
        complete_msg = checkout_page.get_complete_header()
        assert complete_msg == "Thank you for your order!", f"Thông báo hoàn tất không khớp! Thực tế: {complete_msg}"
        assert checkout_page.is_back_home_button_displayed(), "Nút 'Back Home' không hiển thị!"
        print(f"\n[TC05 PASS] Quy trình đặt hàng hoàn tất thành công với thông báo: '{complete_msg}'")

    def test_tc06_logout_success(self, driver):
        """
        TC06: Kiểm tra đăng xuất thành công khỏi hệ thống.
        - Các bước: Mở menu điều hướng (burger menu) -> Bấm Logout.
        - Kỳ vọng: Hệ thống điều hướng quay trở lại trang đăng nhập (saucedemo.com) và nút Login hiển thị.
        """
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("standard_user", "secret_sauce")

        inventory_page = InventoryPage(driver)
        inventory_page.wait_for_url("inventory.html")

        # Thực hiện logout
        inventory_page.logout()

        # Chờ và kiểm tra trang quay lại login
        login_page.wait_for_url("https://www.saucedemo.com/")
        assert login_page.is_login_button_displayed(), "Không tìm thấy nút đăng nhập sau khi logout!"
        print("\n[TC06 PASS] Đăng xuất thành công, đã quay về trang Login.")
