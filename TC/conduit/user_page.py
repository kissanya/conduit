from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from general_functions import *
from login_user import LoginUser


class UserPage(LoginUser):
    def __init__(self, user_data=default_user):
        try:
            super().__init__(user_data)
            self.sign_in(user_data["email"], user_data["password"], user_data["user_name"])
        except Exception as e:
            print(e)
            raise e

    def my_feed_link(self):
        return self.browser.find_element(By.LINK_TEXT, "#/my-feed")

    def global_feed_link(self):
        return self.browser.find_element(By.LINK_TEXT, "#/")

    def get_article_previews(self):
        return self.browser.find_elements(By.CLASS_NAME, 'article-preview')

    def article_page_links(self):
        pages_links = self.get_elements((By.XPATH, "//ul[@class='pagination']/li/a"))
        assert pages_links
        return pages_links

    def articles_parent(self):
        return self.get_element((By.XPATH, '//div[@class = "home-global"]/div/div'))

    def article_preview_users(self):
        return self.get_elements((By.XPATH, '//div[@class="article-meta"]/div[@class="info"]/a[text()]'))

    def article_preview_titles(self):
        return self.get_elements((By.XPATH, '//div[@class="article-preview"]/a[@class="preview-link"]/h1'))

    def article_preview_dates(self):
        return self.get_elements((By.XPATH,
                                  '//div[@class="article-meta"]/div[@class="info"]/span[@class = "date"]'))

    def article_preview_summaries(self):
        return self.get_elements((By.XPATH, '//div[@class="article-preview"]/a[@class="preview-link"]/p'))

    def article_preview_tags(self, index):
        locator = f'//div[@class = "home-global"]/div/div/div[{index+1}]/a/div[@class="tag-list"]/a'
        return self.get_elements(
            (By.XPATH,locator))

    def article_page_link(self, page_index):
        xpath_expression = f"//ul[@class='pagination']/li/a[@class='page-link' and text()='{page_index}']"
        page_link = self.wait_element_located((By.XPATH, xpath_expression))
        assert page_link
        return page_link

    def articles_previews_browse(self):
        data = []
        result = True
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
                result = result and self.extract_previews_data(data)
            else:
                result = False
        return result, data

    def extract_previews_data(self, data):
        users = self.article_preview_users()
        titles = self.article_preview_titles()
        summaries = self.article_preview_summaries()
        dates = self.article_preview_dates()
        for index_user in range(len(users)):
            try:
                tags = [element.text for element in self.article_preview_tags(index_user)]
                data_to_save = (users[index_user].text,
                                titles[index_user].text,
                                summaries[index_user].text,
                                dates[index_user].text,
                                tags
                                )
                data.append(data_to_save)
                print(data_to_save)
            except StaleElementReferenceException as e:
                print(f"Error: {e} occured")
                return False
        return True

    def save_article_previews(self) -> (bool, str):
        with open(article_previews_file, 'w', encoding='UTF-8', newline='') as datafile:
            writer = csv.writer(datafile)
            result, previews = self.articles_previews_browse()
            if result:
                writer.writerow(('User',"Title","Summary","Date","Tags"))
                for row in previews:
                    writer.writerow(row)
                _message = f"Mentés megtörtént a {article_previews_file} fájlba"
            else:
                _message = f"Mentés sikertelen, a bejárás sikertelen."
        return result, _message


if __name__ == "__main__":
    user_page = UserPage()
    message = ""
    user_page.save_article_previews()
    user_page.close()
