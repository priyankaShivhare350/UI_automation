import time

from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class AuthPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    my_account=(By.CSS_SELECTOR,"[href$='my-account/']")
    reg_email = (By.ID, "reg_email")
    reg_password = (By.ID, "reg_password")
    register_button = (By.NAME, "register")
    login_email = (By.ID, "username")
    login_password = (By.ID, "password")
    login_button = (By.NAME, "login")
    error_message = (By.CSS_SELECTOR, "[class$=error]")
    logout_link = (By.LINK_TEXT, "Logout")
    weak_pwd_alert=(By.CSS_SELECTOR,"#reg_password + div")

    def go_to_my_account(self):
        self.click(self.my_account)

    def register(self, email, password):
        self.enter_text(self.reg_email, email)
        self.enter_text(self.reg_password, password)
        self.click(self.register_button)

    def login(self, email, password):
        self.enter_text(self.login_email, email)
        self.enter_text(self.login_password, password)
        self.click(self.login_button)

    def get_error_message(self):
        return self.get_element_text(self.error_message)

    def is_logout_present(self):
        return self.is_element_displayed(self.logout_link)

    def is_weak_pwd_alert(self):
        return self.is_element_displayed(self.weak_pwd_alert)

    def enter_username_pwd(self,username,password):
        self.enter_text(self.login_email, username)
        self.enter_text(self.reg_password, password)

    def is_register_disabled(self):
        return self.is_element_disabled(self.register_button)