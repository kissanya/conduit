import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

import configuration as config
from general_page import GeneralPage
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from general_functions import get_new_user_name, get_users_from_file, create_users_file


class UserRegistration(GeneralPage):
    user_url = "http://localhost:1667/#/register"

    def __init__(self):
        super().__init__(config.get_chrome_driver(), self.user_url)
        self.open()

    def input_email(self):
        email_element = self.browser.find_element(By.XPATH, '//input[@placeholder="Email"]')
        return email_element

    def input_username(self):
        username_element = self.browser.find_element(By.XPATH, '//input[@placeholder="Username"]')
        return username_element

    def input_password(self):
        password_element = self.browser.find_element(By.XPATH, '//input[@placeholder="Password"]')
        return password_element

    def submit_user(self) -> WebElement:
        try:
            button = WebDriverWait(self.browser, 10).until(
                ec.presence_of_element_located((By.XPATH, '//button[contains(text(), "Sign up")]')))
            return button
        except:
            return None

    def message_acknowledge(self):
        button = WebDriverWait(self.browser, 10).until(
            ec.presence_of_element_located((By.CLASS_NAME, 'swal-button--confirm')))
        button.click()

    def register_user(self, _username: str, _email: str, _password: str) -> bool:
        """
            :returns Új felhasználó felvétele és ellenőrzése  UI szinten
        """
        self.url = self.user_url
        self.open()
        if self.submit_user().is_displayed():
            self.input_email().clear()
            self.input_password().clear()
            self.input_username().clear()

            self.input_email().send_keys(_email)
            self.input_password().send_keys(_password)
            self.input_username().send_keys(_username)
            self.submit_user().click()

        result = self.check_valid_registration()
        if result:
            self.message_acknowledge()
        return result

    def check_valid_registration(self) -> bool:
        div = None
        try:
            div = WebDriverWait(self.browser, 5, 1).until(
                ec.presence_of_element_located((By.XPATH, "//div[text()='Your registration was successful!']")))
        except Exception as e:
            print(e)
        if isinstance(div, type(None)):
            return False
        else:
            return True

    def check_invalid_registration(self) -> bool:
        div = WebDriverWait(self.browser, 5).until(
            lambda x: x.find_element(By.CLASS_NAME, 'swal-icon--error'))
        return div.is_displayed()

    def register_users_from_file(self):
        result = True
        create_users_file()
        for user in get_users_from_file():
            user_id, user_name, email, password = user
            result = result and self.register_user(user_name, email, password)
            if result:
                allure.dynamic.description(f"{user_name} felhasználó létrehozva")
            else:
                allure.dynamic.description(f"{user_name} felhasználó létrehozása sikertelen")
        return result


if __name__ == '__main__':
    user_page = UserRegistration()
    user_name = get_new_user_name(0)
    email = user_name + "@testmail.com"
    password = 'Password_01.'
    assert user_page.register_user(user_name, email, password)
    user_page.register_users_from_file()
    user_page.close()
