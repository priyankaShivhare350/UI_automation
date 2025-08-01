import os
from datetime import datetime

import pytest
import pytest_html
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from utils import config

# Add browser choice
def pytest_addoption(parser):
    parser.addoption(
        "--browser_name", action="store", default="chrome", help="browser selection"
    )

# Initialize driver
@pytest.fixture(scope="function",autouse=True)
def driver(request):
    browser_name = request.config.getoption("browser_name")
    service_obj = Service()
    driver = webdriver.Chrome(service=service_obj)
    driver.implicitly_wait(5)
    driver.maximize_window()
    request.node.driver = driver
    driver.get(config.BASE_URL)
    driver.set_page_load_timeout(30)
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



