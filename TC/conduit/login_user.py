import time

from selenium.common import TimeoutException
from main_page import MainPage
from data_layer import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class LoginUser(MainPage):

    def __init__(self):
        super().__init__()
        register_default_user()
        self.sign_in_button().click()
        assert self.sign_in_present()

    def sign_in_present(self):
        return WebDriverWait(self.browser, 5).until(ec.url_matches("http://localhost:1667/#/login"))

    def user_logged_in(self, user):
        xpath = f"//a[@href='#/@{user}/']"

        try:
            link = WebDriverWait(self.browser, 1).until(ec.presence_of_element_located((By.XPATH, xpath)))
            return link.is_displayed()
        except TimeoutException as e:
            return False

    def logged_out(self):
        return self.sign_in_link_exists()

    def input_email(self):
        return self.browser.find_element(By.XPATH, '//input[@placeholder="Email"]')

    def input_password(self):
        return self.browser.find_element(By.XPATH, '//input[@type="password"]')

    def button_sign_in(self):
        return self.browser.find_element(By.XPATH, '//button[@class="btn btn-lg btn-primary pull-xs-right"]')

    def button_logout(self):
        return self.browser.find_element(By.CLASS_NAME, 'ion-android-exit')

    def logout(self):
        if not self.logged_out():
            self.button_logout().click()
            return True
        else:
            return False

    def sign_in(self, _email, _password, _user_name):
        email = self.input_email()
        password = self.input_password()
        email.clear()
        password.clear()
        email.send_keys(_email)
        password.send_keys(_password)
        self.button_sign_in().click()
        return self.user_logged_in(_user_name)


if __name__ == '__main__':
    login_page = LoginUser()
    print(login_page.sign_in(default_user["email"], default_user["password"], default_user["user_name"]))
    time.sleep(1)
    login_page.logout()
    login_page.close()
