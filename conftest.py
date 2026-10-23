import os
import pytest
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def pytest_addoption(parser):
    """Thêm tham số dòng lệnh tùy chọn cho pytest."""
    parser.addoption(
        "--headless",
        action="store",
        default="true",
        help="Chạy trình duyệt Chrome ở chế độ headless (true/false)",
    )


@pytest.fixture(scope="function")
def driver(request):
    """Fixture khởi tạo trình duyệt Chrome trước mỗi test case và tự động đóng sau khi test xong."""
    headless_opt = request.config.getoption("--headless").lower() == "true"

    options = Options()
    if headless_opt:
        options.add_argument("--headless=new")
    
    # Các options tối ưu hiệu năng và tính ổn định
    options.add_argument("--start-maximized")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    # Kiểm tra driver path nếu có trong cache selenium
    cached_driver = r"C:\Users\dagdt\.cache\selenium\chromedriver\win64\155.0.8059.84\chromedriver.exe"
    if os.path.exists(cached_driver):
        service = Service(cached_driver)
        driver_instance = webdriver.Chrome(service=service, options=options)
    else:
        driver_instance = webdriver.Chrome(options=options)

    driver_instance.implicitly_wait(2)

    yield driver_instance

    # Teardown: Chụp ảnh màn hình lưu vào thư mục reports nếu có lỗi hoặc kết thúc
    reports_dir = os.path.join(os.path.dirname(__file__), "reports", "screenshots")
    os.makedirs(reports_dir, exist_ok=True)
    test_name = request.node.name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = os.path.join(reports_dir, f"{test_name}_{timestamp}.png")
    
    try:
        driver_instance.save_screenshot(screenshot_path)
    except Exception:
        pass

    driver_instance.quit()
