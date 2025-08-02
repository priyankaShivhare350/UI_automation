import time

import pytest
from conftest import generate_random_email
from pages.auth_page import AuthPage
from pages.address_page import AddressPage
from utils import data

# Generate once globally

email = generate_random_email()

@pytest.mark.address
class TestAddress:
    @pytest.mark.runow
    def test_add_billing_and_shipping_address(self, driver):
        auth_page = AuthPage(driver)
        auth_page.go_to_my_account()
        address_page = AddressPage(driver)
        # Register new user
        password = data.valid_user["password"]
        auth_page.register(email, password)

        # Add Billing Address
        address_page.navigate_to_addresses()
        address_page.edit_billing()
        address_page.fill_billing_address(data.address)
        address_page.save_address()
        address_page.assert_success_message(address_page.get_success_message())

        address_page.navigate_to_addresses()
        billing_text = address_page.get_billing_address_text()
        address_page.assert_address_in_text(data.address, billing_text)

        # Add Shipping Address
        address_page.edit_shipping()
        address_page.fill_shipping_address(data.address)
        address_page.save_address()
        address_page.assert_success_message(address_page.get_success_message())

        address_page.navigate_to_addresses()
        shipping_text = address_page.get_shipping_address_text()
        address_page.assert_address_in_text(data.address, shipping_text)

    def test_edit_billing_address(self, driver):
        auth_page = AuthPage(driver)
        auth_page.go_to_my_account()
        address_page = AddressPage(driver)
        # Login with the same global email
        auth_page.login(email, data.valid_user["password"])
        # Edit Billing Address
        address_page.navigate_to_addresses()
        address_page.edit_billing()
        address_page.fill_billing_address(data.updated_address)
        address_page.save_address()
        address_page.assert_success_message(address_page.get_success_message())

        address_page.navigate_to_addresses()
        billing_text = address_page.get_billing_address_text()
        address_page.assert_address_in_text(data.updated_address, billing_text)

    def test_edit_shipping_address(self, driver):
        global email
        auth_page = AuthPage(driver)
        auth_page.go_to_my_account()
        address_page = AddressPage(driver)

        # Login with the same global email
        auth_page.login(email, data.valid_user["password"])

        # Edit Shipping Address
        address_page.navigate_to_addresses()
        address_page.edit_shipping()
        address_page.fill_shipping_address(data.updated_address)
        address_page.save_address()
        address_page.assert_success_message(address_page.get_success_message())

        address_page.navigate_to_addresses()
        shipping_text = address_page.get_shipping_address_text()
        address_page.assert_address_in_text(data.updated_address, shipping_text)

    def test_address_persistence_after_navigation(self, driver):
        auth_page = AuthPage(driver)
        auth_page.go_to_my_account()
        address_page = AddressPage(driver)

        auth_page.login(email, data.valid_user["password"])

        address_page.navigate_to_addresses()
        address_page.edit_shipping()
        address_page.fill_shipping_address(data.address)
        address_page.save_address()

        # Navigate away and return
        address_page.go_to_dashboard()
        address_page.navigate_to_addresses()
        shipping_text = address_page.get_shipping_address_text()

        address_page.assert_address_in_text(data.address, shipping_text)

    def test_address_with_optional_fields_blank(self, driver):
        auth_page = AuthPage(driver)
        auth_page.go_to_my_account()
        address_page = AddressPage(driver)

        auth_page.login(email, data.valid_user["password"])

        # Clear optional fields
        optional_blank_data = data.address.copy()
        optional_blank_data["company"] = ""

        address_page.navigate_to_addresses()
        address_page.edit_billing()
        address_page.fill_billing_address(optional_blank_data)
        address_page.save_address()
        address_page.assert_success_message(address_page.get_success_message())
        address_page.navigate_to_addresses()
        billing_text = address_page.get_billing_address_text()
        address_page.assert_address_in_text(optional_blank_data, billing_text)

    @pytest.mark.runow
    def test_address_required_fields_blank(self, driver):
        auth_page = AuthPage(driver)
        auth_page.go_to_my_account()
        address_page = AddressPage(driver)
        auth_page.login(email, data.valid_user["password"])
        address_page.navigate_to_addresses()
        address_page.edit_shipping()
        address_page.fill_shipping_address(data.required_blank_address)
        address_page.save_address()
        error_messages = address_page.get_all_error_messages()
        expected_errors = [
            "First Name is a required field.",
            "Last Name is a required field.",
            "Address is a required field.",
            "Town / City is a required field.",
            "Postcode / ZIP is a required field.",
        ]
        assert sorted(error_messages) == sorted(expected_errors), "Error messages do not match expected."

    def test_address_whitespace_only_fields(self, driver):
        auth_page = AuthPage(driver)
        auth_page.go_to_my_account()
        address_page = AddressPage(driver)
        auth_page.login(email, data.valid_user["password"])
        address_page.navigate_to_addresses()
        address_page.edit_billing()
        address_page.fill_billing_address(data.whitespace_address)
        address_page.save_address()
        error_messages = address_page.get_all_error_messages()
        expected_errors = [
            "First Name is a required field.",
            "Last Name is a required field.",
            "Address is a required field.",
            "Town / City is a required field.",
            "Postcode / ZIP is a required field.",
            "Phone is a required field."
        ]
        assert sorted(error_messages) == sorted(expected_errors), "Whitespace validation failed."

