import os
from datetime import datetime
import random, string
import pytest
import pytest_html
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from utils import config
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

# Add browser choice
def pytest_addoption(parser):
    parser.addoption(
        "--browser_name", action="store", default="chrome", help="browser selection"
    )
    parser.addoption(
        "--headless", action="store_true", default=False, help="run in headless mode"
    )

# Initialize driver
@pytest.fixture(scope="function",autouse=True)
def driver(request):
    browser_name = request.config.getoption("browser_name")
    headless = request.config.getoption("headless")
    if browser_name == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")  # new mode avoids deprecation warning
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(service=ChromeService(), options=options)
    elif browser_name == "firefox":
        options = FirefoxOptions()
        if headless:
            options.headless = True
        driver = webdriver.Firefox(service=FirefoxService(), options=options)
    elif browser_name == "edge":
        options = EdgeOptions()
        if headless:
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
        driver = webdriver.Edge(service=EdgeService(), options=options)
    else:
        raise ValueError(f"Browser '{browser_name}' is not supported. Use chrome, firefox, or edge.")
    driver.implicitly_wait(5)
    driver.set_window_size(1920, 1080)
    driver.set_page_load_timeout(30)
    driver.get(config.BASE_URL)
    request.node.driver = driver
    yield driver
    driver.quit()

# Hook to add screenshot on failure
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])

    if report.when == "call" and report.failed:
        driver = getattr(item, "driver", None)
        if driver:
            screenshots_dir = os.path.join(os.path.dirname(__file__), "reports", "screenshots")
            os.makedirs(screenshots_dir, exist_ok=True)
            file_name = os.path.join(screenshots_dir, f"{item.name}.png")
            driver.save_screenshot(file_name)
            html = (
                f'<div><img src="{file_name}" alt="screenshot" '
                f'style="width:300px;height:200px;" '
                f'onclick="window.open(this.src)" align="right"/></div>'
            )
            extra.append(pytest_html.extras.html(html))
        report.extra = extra


def generate_random_email():
    prefix = ''.join(random.choices(string.ascii_lowercase, k=6))
    return f"{prefix}@gamil.com"


