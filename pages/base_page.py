from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
import time

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def click(self, by_locator):
        element = self.wait.until(EC.element_to_be_clickable(by_locator))
        self.driver.execute_script("arguments[0].click();", element)

    def enter_text(self, by_locator, text):
        element = self.wait.until(EC.visibility_of_element_located(by_locator))
        element.clear()
        element.send_keys(text)

    def get_element_text(self, by_locator):
        return self.wait.until(EC.visibility_of_element_located(by_locator)).text

    def is_element_displayed(self, by_locator):
        return self.wait.until(EC.visibility_of_element_located(by_locator)).is_displayed()

    def get_attribute(self, by_locator, attribute):
        return self.wait.until(EC.presence_of_element_located(by_locator)).get_attribute(attribute)

    def hover_over_element(self, by_locator):
        element = self.wait.until(EC.visibility_of_element_located(by_locator))
        ActionChains(self.driver).move_to_element(element).perform()

    def double_click(self, by_locator):
        element = self.wait.until(EC.element_to_be_clickable(by_locator))
        ActionChains(self.driver).double_click(element).perform()

    def right_click(self, by_locator):
        element = self.wait.until(EC.element_to_be_clickable(by_locator))
        ActionChains(self.driver).context_click(element).perform()

    def select_dropdown_by_value(self, by_locator, value):
        select = Select(self.wait.until(EC.element_to_be_clickable(by_locator)))
        select.select_by_value(value)

    def select_dropdown_by_visible_text(self, by_locator, text):
        select = Select(self.wait.until(EC.element_to_be_clickable(by_locator)))
        select.select_by_visible_text(text)

    def accept_alert(self):
        self.wait.until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        alert.accept()

    def dismiss_alert(self):
        self.wait.until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        alert.dismiss()

    def upload_file(self, by_locator, file_path):
        self.wait.until(EC.presence_of_element_located(by_locator)).send_keys(file_path)

    def scroll_into_view(self, by_locator):
        element = self.wait.until(EC.presence_of_element_located(by_locator))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def click_with_js(self, by_locator):
        element = self.wait.until(EC.element_to_be_clickable(by_locator))
        self.driver.execute_script("arguments[0].click();", element)

    def take_screenshot(self, file_name):
        self.driver.save_screenshot(file_name)

    def wait_for_element_invisible(self, by_locator):
        self.wait.until(EC.invisibility_of_element_located(by_locator))

    def is_checkbox_checked(self, by_locator):
        return self.wait.until(EC.element_to_be_clickable(by_locator)).is_selected()

    def check_checkbox(self, by_locator):
        checkbox = self.wait.until(EC.element_to_be_clickable(by_locator))
        if not checkbox.is_selected():
            checkbox.click()

    def uncheck_checkbox(self, by_locator):
        checkbox = self.wait.until(EC.element_to_be_clickable(by_locator))
        if checkbox.is_selected():
            checkbox.click()

    def get_text(self, locator):
        return self.driver.find_element(*locator).text
