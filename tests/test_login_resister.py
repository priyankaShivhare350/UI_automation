import pytest
from conftest import generate_random_email
from pages.auth_page import AuthPage
from utils import data


@pytest.mark.register
class TestRegistration:

    def test_successful_registration(self, driver):
        auth_page = AuthPage(driver)
        auth_page.go_to_my_account()
        email = generate_random_email()
        password = data.valid_user["password"]
        auth_page.register(email, password)
        assert auth_page.is_logout_present()

    def test_registration_with_existing_email(self, driver):
        auth_page = AuthPage(driver)
        auth_page.go_to_my_account()
        email = data.valid_user["email"]
        password = data.valid_user["password"]
        auth_page.register(email, password)
        expected_msg = "Error: An account is already registered with your email address. Please login."
        actual_msg = auth_page.get_error_message().lower()
        assert expected_msg.lower() in actual_msg, f"Actual message is {actual_msg}"

    def test_registration_with_blank_fields(self, driver):
        auth_page = AuthPage(driver)
        auth_page.go_to_my_account()
        # Blank email and password
        auth_page.register("", "")
        assert "please provide a valid email address" in auth_page.get_error_message().lower()

        # Blank password
        auth_page.register("random@random.com", "")
        assert "please enter an account password" in auth_page.get_error_message().lower()

        # Blank email
        auth_page.register("", data.valid_user["password"])
        assert "please provide a valid email address" in auth_page.get_error_message().lower()

    def test_registration_with_weak_password(self, driver):
        auth_page = AuthPage(driver)
        auth_page.go_to_my_account()
        email = generate_random_email()
        password = "123"
        auth_page.enter_username_pwd(email, password)
        assert auth_page.is_register_disabled()
        assert auth_page.is_weak_pwd_alert()

    def test_registration_with_invalid_email_and_password(self, driver):
        auth_page = AuthPage(driver)
        auth_page.go_to_my_account()
        email = "invalid"
        password = "123"
        auth_page.enter_username_pwd(email, password)
        assert auth_page.is_register_disabled()
        assert auth_page.is_weak_pwd_alert()


@pytest.mark.login
class TestLogin:

    def test_successful_login(self, driver):
        auth_page = AuthPage(driver)
        auth_page.go_to_my_account()
        auth_page.login(data.valid_user["email"], data.valid_user["password"])
        assert auth_page.is_logout_present()

    def test_login_with_wrong_password(self, driver):
        auth_page = AuthPage(driver)
        auth_page.go_to_my_account()
        auth_page.login(data.valid_user["email"], "wrongpass")
        expected = f"error: the password you entered for the username {data.valid_user['email']} is incorrect. lost your password?"
        actual = auth_page.get_error_message().lower()
        assert expected in actual, f"Actual message is {actual}"

    def test_login_with_invalid_email_format(self, driver):
        auth_page = AuthPage(driver)
        auth_page.go_to_my_account()
        auth_page.login("invalidemail", data.valid_user["password"])
        expected = "error: the password you entered for the username invalidemail is incorrect. lost your password?"
        actual = auth_page.get_error_message().lower()
        assert expected in actual, f"Actual message is {actual}"

    def test_login_with_unregistered_email(self, driver):
        auth_page = AuthPage(driver)
        auth_page.go_to_my_account()
        auth_page.login("unregistered@example.com", data.valid_user["password"])
        expected = "error: a user could not be found with this email address."
        actual = auth_page.get_error_message().lower()
        assert expected in actual, f"Actual message is {actual}"

    def test_login_with_blank_fields(self, driver):
        auth_page = AuthPage(driver)
        auth_page.go_to_my_account()
        auth_page.login("", "")
        expected = "error: username is required."
        actual = auth_page.get_error_message().lower()
        assert expected in actual, f"Actual message is {actual}"
