from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC

class AddressPage(BasePage):
    # Common Locators
    ADDRESSES_LINK = (By.LINK_TEXT, "Addresses")
    EDIT_BILLING = (By.LINK_TEXT, "Edit")
    EDIT_SHIPPING = (By.XPATH, "(//a[text()='Edit'])[2]")
    SAVE_BUTTON = (By.CSS_SELECTOR, '[name="save_address"]')
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, "div.woocommerce-message")
    dashboard=(By.LINK_TEXT, "Dashboard")
    error_message=(By.CSS_SELECTOR, ".woocommerce-error li")
    # Billing Display
    BILLING_ADDRESS_DISPLAY = (By.XPATH, "//*[text()='Billing Address']/../following-sibling::address")
    # Shipping Display
    SHIPPING_ADDRESS_DISPLAY = (By.XPATH, "//*[text()='Shipping Address']/../following-sibling::address")

    # Billing Form Fields
    FIRST_NAME = (By.ID, "billing_first_name")
    LAST_NAME = (By.ID, "billing_last_name")
    COMPANY = (By.ID, "billing_company")
    ADDRESS1 = (By.ID, "billing_address_1")
    CITY = (By.ID, "billing_city")
    POSTCODE = (By.ID, "billing_postcode")
    PHONE = (By.ID, "billing_phone")

    # Shipping Form Fields
    SHIPPING_FIRST_NAME = (By.ID, "shipping_first_name")
    SHIPPING_LAST_NAME = (By.ID, "shipping_last_name")
    SHIPPING_COMPANY = (By.ID, "shipping_company")
    SHIPPING_ADDRESS1 = (By.ID, "shipping_address_1")
    SHIPPING_CITY = (By.ID, "shipping_city")
    SHIPPING_POSTCODE = (By.ID, "shipping_postcode")

    def navigate_to_addresses(self):
        self.click(self.ADDRESSES_LINK)

    def edit_billing(self):
        self.click(self.EDIT_BILLING)

    def edit_shipping(self):
        self.click(self.EDIT_SHIPPING)

    def fill_billing_address(self, address_data: dict):
        self.clear_and_type(self.FIRST_NAME, address_data["first_name"])
        self.clear_and_type(self.LAST_NAME, address_data["last_name"])
        self.clear_and_type(self.COMPANY, address_data.get("company", ""))

        self.clear_and_type(self.ADDRESS1, address_data["address"])
        self.clear_and_type(self.CITY, address_data["city"])
        self.clear_and_type(self.POSTCODE, address_data["postcode"])
        self.clear_and_type(self.PHONE, address_data["phone"])

    def fill_shipping_address(self, address_data: dict):
        self.clear_and_type(self.SHIPPING_FIRST_NAME, address_data["first_name"])
        self.clear_and_type(self.SHIPPING_LAST_NAME, address_data["last_name"])
        self.clear_and_type(self.SHIPPING_COMPANY, address_data.get("company", ""))
        self.clear_and_type(self.SHIPPING_ADDRESS1, address_data["address"])
        self.clear_and_type(self.SHIPPING_CITY, address_data["city"])
        self.clear_and_type(self.SHIPPING_POSTCODE, address_data["postcode"])

    def save_address(self):
        self.click(self.SAVE_BUTTON)

    def get_success_message(self):
        return self.get_text(self.SUCCESS_MESSAGE)

    def get_displayed_billing_address(self):
        return self.get_text(self.BILLING_ADDRESS_DISPLAY)

    def get_displayed_shipping_address(self):
        return self.get_text(self.SHIPPING_ADDRESS_DISPLAY)

    def get_billing_address_text(self):
        return self.get_displayed_billing_address()

    def get_shipping_address_text(self):
        return self.get_displayed_shipping_address()

    def assert_address_in_text(self,expected, actual_text):
        for key, value in expected.items():
            if key != "phone":
                assert value in actual_text, f"Expected '{value}' for '{key}' not found in address text."

    def assert_success_message(self,actual_message, expected_message="Address changed successfully."):
        assert expected_message in actual_message, f"Expected message '{expected_message}' not found"

    def get_all_error_messages(self):
        try:
            error_elements = self.driver.find_elements(By.CSS_SELECTOR, ".woocommerce-error li")
            return [elem.text.strip() for elem in error_elements]
        except Exception as e:
            print(f"[Error] While fetching error messages: {e}")
            return []

    def go_to_dashboard(self):
        self.click(self.dashboard)
