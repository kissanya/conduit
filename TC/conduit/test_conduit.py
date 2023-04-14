import main_page
import register_user as register
import login_user as login
import allure

from configuration import *


class TestMain:

    def setup_method(self):
        self.page = main_page.MainPage()

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


class TestRegistration:

    def setup_method(self):
        self.page = register.UserRegistration()

    def teardown_method(self):
        self.page.close()

    @allure.id('TC3')
    @allure.epic("Felhasználó kezelés")
    @allure.title('Új felhasználó rögzítése')
    @allure.description('Új felhasználónév, email, jelszó generálása, és regisztrációja a conduit felületen')
    def test_create_single_user(self):
        user_name = register.get_new_user_name(0)
        email = user_name + "@testmail.com"
        password = 'Password_01.'
        assert self.page.register_user(user_name, email, password)

    @allure.id('TC4')
    @allure.epic("Felhasználó kezelés")
    @allure.title('10 új felhasználó rögzítése')
    @allure.description('Új felhasználónév, email, jelszó generálása, és regisztrációja a conduit felületen')
    def test_create_single_user(self):
        assert self.page.register_users_from_file()


class TestLogin:

    def setup_method(self):
        self.page = login.LoginUser()

    def teardown_method(self):
        self.page.close()

    @allure.id('TC5')
    @allure.epic("Felhasználó kezelés")
    @allure.title('Létező felhasználó bejelentkezése')
    @allure.description(f'A létrehozott <strong>{default_user["user_name"]}</strong> felhasználó bejelentkeztetése')
    def test_login_user(self):
        assert self.page.sign_in()
