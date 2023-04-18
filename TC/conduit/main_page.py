from selenium.webdriver.remote.webelement import WebElement

from general_page import GeneralPage
import configuration as config
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class MainPage(GeneralPage):

    def __init__(self):
        super().__init__(config.get_chrome_driver(), "http://localhost:1667")
        self.open()

    def logo(self) -> WebElement:
        return self.browser.find_element(By.CLASS_NAME, 'logo-font')

    def policy_panel(self):
        """
        Adatvédelmi panel lekérése
        :return: ha létezik visszaadja a Panelt
        """
        panels = self.browser.find_elements(By.ID, 'cookie-policy-panel')
        if len(panels) > 0:
            return panels[0]

    def sign_in_button(self):
        return self.browser.find_element(By.XPATH, '//a[@href="#/login"]')

    def sign_in_link_exists(self):
        try:
            element = self.sign_in_button()
            return True
        except:
            return False

    def policy_accept_button(self):
        return self.browser.find_element(By.CLASS_NAME,
                                         'cookie__bar__buttons__button--accept')

    def policy_decline_button(self):
        return self.browser.find_element(By.CLASS_NAME,
                                         'cookie__bar__buttons__button--decline')

    def accept_data_policy(self) -> bool:
        panel = self.policy_panel()
        if panel.is_displayed():
            self.policy_accept_button().click()
        is_not_present = WebDriverWait(self.browser, 5).until_not(
            lambda x: x.find_element(By.ID, 'cookie-policy-panel'))
        return is_not_present


if __name__ == '__main__':
    main = MainPage()
    print(main.accept_data_policy())
    main.close()
