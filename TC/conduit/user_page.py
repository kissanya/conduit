from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

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

    def article_page_link(self, page_index):
        xpath_expression = f"//ul[@class='pagination']/li/a[@class='page-link' and text()='{page_index}']"
        page_link = WebDriverWait(user_page.browser, 5).until(
            ec.presence_of_element_located((By.XPATH, xpath_expression)))
        assert page_link
        return page_link

    def article_users(self):
        return self.browser.find_elements(By.XPATH, '//div[@class="article-meta"]/div[@class="info"]/a[text()]')

    def article_titles(self):
        return self.browser.find_elements(By.XPATH, '//div[@class="article-preview"]/a[@class="preview-link"]/h1')

    def article_body(self):
        return self.browser.find_elements(By.XPATH, '//div[@class="article-preview"]/a[@class="preview-link"]/h1')


if __name__ == "__main__":
    user_page = UserPage()
    pages = len(user_page.article_page_links())
    for index_page in range(1, pages + 1):
        page = user_page.article_page_link(index_page)
        page.click()
        page = user_page.article_page_link(index_page)

        active_link = WebDriverWait(user_page.browser, 5).until(
            ec.presence_of_element_located(
                (By.XPATH, f'//li[@class="page-item active"]/a[@class="page-link" and text()="{index_page}"]')))

        if page.text == active_link.text:
            users = (user_page.article_users())
            titles = (user_page.article_titles())
            for index_user in range(len(users)):
                print(users[index_user].text, titles[index_user].text)
    user_page.close()
