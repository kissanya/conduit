import datetime

from selenium.webdriver.common.by import By
import TC.globals.configuration as config
from TC.globals.general_page import GeneralPage
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Registration(GeneralPage):
    def __init__(self):
        super().__init__(config.get_chrome_driver(), "http://localhost:1667/#/register")
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

    def submit(self):
        submit_buttons = self.browser.find_elements(By.XPATH, '//button[contains(text(), "Sign up")]')
        if len(submit_buttons) > 0:
            return submit_buttons[0]

    def register_user(self, _username, _email, _password) -> bool:
        self.input_email().send_keys(_email)
        self.input_password().send_keys(_password)
        self.input_username().send_keys(_username)
        self.submit().click()
        return self.check_valid_registration()

    def check_valid_registration(self) -> bool:
        div = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'swal-text')))
        print(div.text)
        return div.text == "Your registration was successful!"

    def check_invalid_registration(self) -> bool:
        div = WebDriverWait(self.browser, 5).until(
            lambda x: x.find_element(By.CLASS_NAME, 'swal-icon--error'))
        return div.is_displayed()


if __name__ == '__main__':
    new_user = Registration()
    user_name = 'testuser' + str(datetime.datetime.now()).replace(":", "").replace("-", "").replace(".", "").replace(
        " ", "")
    email = user_name + "@testmail.com"
    password = 'Password_01.'
    assert new_user.register_user(user_name, email, password)
    new_user.close()
