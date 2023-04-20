from selenium.webdriver.common.by import By
from general_functions import *
from user_page import UserPage


class UserData(UserPage):
    def __init__(self):

        self.user_name =get_new_user_name(12)
        self.picture =""
        self.bio = ""
        self.email = get_new_email(self.user_name)
        self.password = get_new_password(self.user_name)

        user_data = {
            "user_name": self.user_name,
            "email":self.email,
            "password":self.password
        }

        super().__init__(user_data)

        self.accept_data_policy()
        self.settings_link().click()
        self.save_user_tags()
        try:
            assert self.wait_for_url("http://localhost:1667/#/settings")
        except AssertionError as e:
            print(e)


    def save_user_tags(self):
        self.user_name = self.username_input().get_attribute('value')
        self.picture = self.picture_input().get_attribute('value')
        self.bio = self.bio_input().get_attribute('value')
        self.email = self.email_input().get_attribute('value')
        self.password = self.password_input().get_attribute('value')
    def settings_link(self):
        return self.get_element((By.XPATH, "//a[@href='#/settings']"))

    def input_by_placeholder(self, placeholder):
        return self.get_element((By.XPATH, f"//input[@placeholder='{placeholder}']"))

    def picture_input(self):
        return self.input_by_placeholder("URL of profile picture")

    def username_input(self):
        return self.input_by_placeholder("Your username")

    def password_input(self):
        return self.input_by_placeholder("Password")

    def email_input(self):
        return self.input_by_placeholder("Email")

    def bio_input(self):
        return self.get_element((By.XPATH, f"//textarea[@placeholder='Short bio about you']"))

    def submit_button(self):
        return self.get_element((By.TAG_NAME, 'button'))

    def ok_button(self):
        return self.get_element((By.XPATH, "//button[@class='swal-button swal-button--confirm']"))

    def change_user_data(self, _username, _password, _bio, _email, _picture):

        self.save_user_tags()
        self.clear_inputs()

        self.bio_input().clear()
        self.bio_input().send_keys(_bio)

        self.email_input().clear()
        self.email_input().send_keys(_email)

        self.username_input().clear()
        self.username_input().send_keys(_username)

        self.picture_input().clear()
        self.picture_input().send_keys(_picture)

        self.password_input().clear()
        self.password_input().send_keys(_password)

        self.submit_button().click()
        self.wait_element_visible("//div[@class='swal-icon swal-icon--success']")
        self.ok_button().click()
        return True

    def clear_inputs(self):
        self.password_input().clear()
        self.bio_input().clear()
        self.email_input().clear()
        self.username_input().clear()
        self.picture_input().clear()


if __name__ == "__main__":
    user_data = UserData()
    user_data.change_user_data('tesztelek_2', 'Password02.', "En vagyok a default test user",
                               'tesztelek_2@tesztelek.hu', user_data.picture)
