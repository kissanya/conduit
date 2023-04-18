from selenium.webdriver.common.by import By

from configuration import default_user
from login_user import LoginUser
from general_functions import *


class ArticleEditor(LoginUser):

    def __init__(self, article):
        super().__init__()
        assert self.sign_in(default_user["email"], default_user["password"], default_user["user_name"])
        self.button_new_article().click()
        WebDriverWait(self.browser, 5).until(lambda x: x.current_url == "http://localhost:1667/#/editor")

    def inputbox(self, placeholder):
        return get_element(self, (By.XPATH, f"//input[@placeholder='{placeholder}']"))

    def input_title(self):
        return self.inputbox("Article Title")

    def input_summary(self):
        return get_element(self, (By.XPATH, "//input[contains(@placeholder,'article about')]"))

    def input_article(self):
        return get_element(self, (By.XPATH, "//textarea[@placeholder='Write your article (in markdown)']"))

    def input_tags(self):
        return self.inputbox("Enter tags")

    def submit(self):
        return get_element(self, (By.XPATH, "//button[@type='submit']"))

    def create_article(self):
        self.input_title().clear()
        self.input_article().clear()
        self.input_summary().clear()
        self.input_tags().clear()

        title = random_strings("title").upper()

        self.input_title().send_keys(title)
        self.input_article().send_keys(random_markdown("article").capitalize())
        self.input_summary().send_keys(random_strings("summary").capitalize())
        self.input_tags().send_keys(random_strings("tags"))
        self.submit().click()
        try:
            WebDriverWait(self.browser, 5).until(
                lambda x: x.current_url == f"http://localhost:1667/#/articles/{title.lower()}")
            return True
        except TimeoutError as te:
            print(f"Hiba: {te}")
            return False


if __name__ == '__main__':
    editor = ArticleEditor()
    editor.create_article()
    # editor.close()
