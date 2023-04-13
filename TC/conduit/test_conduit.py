import main_page as cm
import allure


class TestConduit:

    def setup_method(self):
        self.page = cm.MainPage()

    def teardown_method(self):
        self.page.close()

    @allure.id('TC1')
    @allure.title('Conduit megjelenítése')
    @allure.description('Oldal megnyitása és a logó megjelenésének ellenőrzése')
    def test_load(self):
        assert self.page.logo().is_displayed()

    @allure.id('TC2')
    @allure.title('Conduit adatkezelési nyilatkozat')
    @allure.description('Adatkezelési nyilatkozat megléte és elfogadása')
    def test_data_policy(self):
        assert self.page.accept_data_policy()
