from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By

from configuration import default_user
from general_functions import *
from login_user import LoginUser


class UserPage(LoginUser):
    def __init__(self, user_data = default_user):

        super().__init__(user_data)
        assert self.sign_in(user_data["email"], user_data["password"], user_data["user_name"])

    def my_feed_link(self):
        return self.browser.find_element(By.LINK_TEXT, "#/my-feed")

    def global_feed_link(self):
        return self.browser.find_element(By.LINK_TEXT, "#/")

    def get_article_previews(self):
        return self.browser.find_elements(By.CLASS_NAME, 'article-preview')

    def article_page_links(self):
        pages_links = self.browser.find_elements(By.XPATH, "//ul[@class='pagination']/li/a")
        assert pages_links
        return pages_links

    def article_users(self):
        return self.browser.find_elements(By.XPATH, '//div[@class="article-meta"]/div[@class="info"]/a[text()]')

    def article_titles(self):
        return self.browser.find_elements(By.XPATH, '//div[@class="article-preview"]/a[@class="preview-link"]/h1')

    def articles_parent(self):
        return self.browser.find_element(By.XPATH, '//div[@class = "home-global"]/div/div')

    def article_body(self):
        return self.browser.find_elements(By.XPATH, '//div[@class="article-preview"]/a[@class="preview-link"]/h1')

    def article_page_link(self, page_index):
        xpath_expression = f"//ul[@class='pagination']/li/a[@class='page-link' and text()='{page_index}']"
        page_link = self.wait_element_located((By.XPATH, xpath_expression))
        assert page_link
        return page_link

    def articles_preview(self):
        result = []
        pages = len(self.article_page_links())
        for index_page in range(1, pages + 1):

            page = self.article_page_link(index_page)
            page.click()

            self.wait_not_element_staleness(self.articles_parent())
            page = self.article_page_link(index_page)

            active_link = self.wait_element_located(
                (By.XPATH, f'//li[@class="page-item active"]/a[@class="page-link" and text()="{index_page}"]'))

            print(f"Page {page.text}")

            if page.text == active_link.text:

                users = (self.article_users())
                titles = (self.article_titles())

                for index_user in range(len(users)):
                    try:
                        result.append((users[index_user].text, titles[index_user].text))
                        print((users[index_user].text, titles[index_user].text))
                    except StaleElementReferenceException as e:
                        print(f"Error: {e} occured")
                        return False
        return result

    def save_article_previews(self) -> (bool, str):
        try:
            with open(article_previews_file, 'w', encoding='UTF-8', newline='') as datafile:
                writer = csv.writer(datafile)
                previews = self.articles_preview()
                for row in previews:
                    writer.writerow(row)
            _message = f"Mentés megtörtént a {article_previews_file} fájlba"
            return True, _message
        except Exception as ex:
            _message = f"Sikertelen mentés: {str(ex)}"
            return False, _message


if __name__ == "__main__":
    user_page = UserPage()
    message = ""
    user_page.save_article_previews()
    user_page.close()
