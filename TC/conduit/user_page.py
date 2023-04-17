import time

from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from general_functions import *
from configuration import default_user
from login_user import LoginUser
from selenium.webdriver.support import expected_conditions as ec


class UserPage(LoginUser):
    def __init__(self):
        super().__init__()
        assert self.sign_in(default_user["email"], default_user["password"], default_user["user_name"])

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

    def article_body(self):
        return self.browser.find_elements(By.XPATH, '//div[@class="article-preview"]/a[@class="preview-link"]/h1')

    def article_page_link(self, page_index):
        xpath_expression = f"//ul[@class='pagination']/li/a[@class='page-link' and text()='{page_index}']"
        page_link = WebDriverWait(self.browser, 5).until(
            ec.presence_of_element_located((By.XPATH, xpath_expression)))
        assert page_link
        return page_link

    def articles_preview(self):
        result = []
        pages = len(self.article_page_links())
        for index_page in range(1, pages + 1):

            page = self.article_page_link(index_page)
            start = time.time()
            page.click()
            WebDriverWait(self.browser, 5).until(lambda x: x.execute_script("return document.readyState") == 'complete')
            end = time.time()
            page = self.article_page_link(index_page)
            print(f"Waiting for load page complete: {end - start}")

            active_link = WebDriverWait(self.browser, 5).until(
                ec.presence_of_element_located(
                    (By.XPATH, f'//li[@class="page-item active"]/a[@class="page-link" and text()="{index_page}"]')))

            if page.text == active_link.text:
                temp_result = []
                tries = 0
                while not self.extract_article_preview_elements(temp_result) and tries < 10:
                    temp_result.clear()
                    time.sleep(0.1)
                    print(f"Tries: {tries}")
                    tries+=1
                    continue
                result.extend(temp_result)
        return result

    def extract_article_preview_elements(self, result):
        users = (self.article_users())
        titles = (self.article_titles())

        for index_user in range(len(users)):
            try:
                result.append((users[index_user].text, titles[index_user].text))
            except StaleElementReferenceException as e:
                return  False
        return True

    def save_article_previews(self, message) -> bool:
        try:
            with open(article_previews_file, 'w', encoding='UTF-8', newline='') as datafile:
                writer = csv.writer(datafile)

                for row in self.articles_preview():
                    writer.writerow(row)
            message = f"Mentés megtörtént a {article_previews_file} fájlba"
            return True
        except Exception as ex:
            message = f"Sikertelen mentés: {ex}"
            return False


if __name__ == "__main__":
    user_page = UserPage()
    message = ""
    user_page.save_article_previews(message)
    user_page.close()
