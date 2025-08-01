from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    USERNAME = (By.ID, "username")
    PASSWORD = (By.ID, "password")
    LOGIN_BTN = (By.NAME, "login")

    def login(self, email, password):
        self.enter_text(self.USERNAME, email)
        self.enter_text(self.PASSWORD, password)
        self.click(self.LOGIN_BTN)
