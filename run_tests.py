import os
import sys

# Đảm bảo in ký tự tiếng Việt không bị lỗi encoding trên Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

import pytest


def main():
    """Chạy toàn bộ test case kiểm thử tự động với Pytest và tạo báo cáo HTML."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    reports_dir = os.path.join(base_dir, "reports")
    os.makedirs(reports_dir, exist_ok=True)

    report_file = os.path.join(reports_dir, "report.html")

    args = [
        "-v",
        "-s",
        "--tb=short",
        f"--html={report_file}",
        "--self-contained-html",
        os.path.join(base_dir, "tests"),
    ]

    print("=" * 70)
    print("   BẮT ĐẦU CHẠY KIỂM THỬ TỰ ĐỘNG VỚI SELENIUM WEBDRIVER & PYTEST")
    print(f"   Trang web kiểm thử: https://www.saucedemo.com/")
    print(f"   File báo cáo kết quả sẽ được lưu tại: {report_file}")
    print("=" * 70)

    exit_code = pytest.main(args)

    print("=" * 70)
    if exit_code == 0:
        print("   >>> TẤT CẢ TEST CASES ĐÃ PASS THÀNH CÔNG 100%! <<<")
    else:
        print(f"   >>> CÓ LỖI XẢY RA HOẶC TEST CASE THẤT BẠI (Mã thoát: {exit_code}) <<<")
    print(f"   Mở báo cáo HTML để xem chi tiết: {report_file}")
    print("=" * 70)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
