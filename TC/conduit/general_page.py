from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

import configuration as config


class GeneralPage:

    def __init__(self, browser: webdriver.Chrome, url):
        self.browser = browser
        self.url = url

    def open(self):
        self.browser.get(self.url)
        self.browser.maximize_window()

    def close(self):
        self.browser.delete_all_cookies()
        self.browser.quit()

    def refresh(self):
        self.browser.refresh()

    def save_screen(self, path):
        filename = f'{self.browser.title}-{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.png'
        print(f'Screenshot attempt: {path}\\{filename}')  # path\filename.png --> C:\screenshots\filename.png
        if not self.browser.save_screenshot(f'{path}\\{filename}'):
            print('Screenshot failed.')

    def get_element(self, locator: tuple, seconds=2) -> WebElement:
        """Call -> self.get_element((By.ID, 'elementID'), seconds=N)"""
        return WebDriverWait(self.browser, seconds).until(
            ec.presence_of_element_located(locator)
        )

    def get_elements(self, locator: tuple, seconds=2) -> list[WebElement]:
        """Call -> self.get_elements((By.TAG_NAME, 'input'), seconds=N)"""
        return WebDriverWait(self.browser, seconds).until(
            ec.presence_of_all_elements_located(locator)
        )

    def wait_for_url(self, url) -> bool:
        try:
            WebDriverWait(self.browser, 5).until(
                lambda x: x.current_url == url)
            return True
        except Exception as e:
            print(e)
            return False

    def wait_element_visible(self, xpath) -> bool:
        try:
            WebDriverWait(self.browser, 5).until(
                lambda x: x.find_element(By.XPATH, xpath)).is_displayed()
            return True
        except Exception as e:
            print(e)
            return False

    def wait_not_element_staleness(self, element):
        return WebDriverWait(self.browser, 5).until_not(ec.staleness_of(element))

    def wait_element_located(self, locator):
        return WebDriverWait(self.browser, 5).until(
            ec.presence_of_element_located(locator))


if __name__ == '__main__':
    page = GeneralPage(config.get_chrome_driver(), 'http://localhost:1667')
    page.open()
    page.close()
