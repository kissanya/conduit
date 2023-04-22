from selenium.webdriver.common.by import By
from general_functions import *
from login_user import LoginUser


class ArticleEditor(LoginUser):

    def __init__(self):
        super().__init__(default_user)
        self.current_article = None
        assert self.sign_in(default_user["email"], default_user["password"], default_user["user_name"])
        self.init_article_info()

    def init_article_info(self):
        self.current_article = {"title": "", "url": ""}

    def inputbox(self, placeholder):
        return self.get_element((By.XPATH, f"//input[@placeholder='{placeholder}']"))

    def input_title(self):
        return self.inputbox("Article Title")

    def input_summary(self):
        return self.get_element((By.XPATH, "//input[contains(@placeholder,'article about')]"))

    def input_article(self):
        return self.get_element((By.XPATH, "//textarea[@placeholder='Write your article (in markdown)']"))

    def input_tags(self):
        return self.inputbox("Enter tags")

    def edit_article_button(self, article_title):
        return self.get_element((By.XPATH, f"//a[@href='#/editor/{article_title.lower()}']"))

    def submit_button(self):
        return self.get_element((By.XPATH, "//button[@type='submit']"))

    def delete_button(self):
        return self.get_element((By.XPATH, "//button[@class='btn btn-outline-danger btn-sm']"))

    def create_article(self):
        self.button_new_article().click()
        self.wait_for_url("http://localhost:1667/#/editor")

        self.input_title().clear()
        self.input_article().clear()
        self.input_summary().clear()
        self.input_tags().clear()

        title = random_strings("title").upper()
        self.current_article = {
            "title": title,
            "url": f"http://localhost:1667/#/articles/{title.lower()}"
        }

        self.input_title().send_keys(title)
        self.input_article().send_keys(random_markdown("article").capitalize())
        self.input_summary().send_keys(random_strings("summary").capitalize())
        self.input_tags().send_keys(random_strings("tags"))
        self.submit_button().click()
        try:
            self.wait_for_url(f"{self.current_article['url']}")
            return True
        except TimeoutError as te:
            print(f"Hiba: {te}")
            return False

    def edit_article(self):
        if self.current_article["url"] == "":
            self.create_article()

        self.edit_article_button(self.current_article["title"]).click()
        self.wait_for_url(f"http://localhost:1667/#/editor/{self.current_article['title'].lower()}")
        self.input_article().send_keys(random_markdown("article").lower())
        self.input_title().send_keys(random_strings("title").lower())
        self.input_summary().send_keys(random_strings("summary").lower())
        self.input_tags().send_keys(random_strings("tag").lower())
        self.submit_button().click()
        return self.wait_for_url(self.current_article["url"])

    def delete_article(self):
        if self.current_article["url"] == "":
            self.create_article()
        self.browser.get(self.current_article["url"])
        self.delete_button().click()
        self.init_article_info()
        return self.wait_for_url("http://localhost:1667/#/")


if __name__ == '__main__':
    editor = ArticleEditor()
    editor.delete_article()

    editor.edit_article()

    editor.close()
