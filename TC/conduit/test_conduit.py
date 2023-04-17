import main_page
import register_user as register
import login_user as login
import allure
from user_page import UserPage
from configuration import *
from data_layer import database
from general_functions import *


@allure.epic("Adatkezelési nyilatkozat")
class TestMain:

    def setup_method(self):
        self.page = main_page.MainPage()

    def teardown_method(self):
        self.page.close()

    @allure.id('TC1')
    @allure.title('Conduit megjelenítése')
    @allure.description(allure_default_descriptions["TC1"])
    def test_load(self):
        assert self.page.logo().is_displayed()

    @allure.id('TC2')
    @allure.title('Conduit adatkezelési nyilatkozat')
    @allure.description('Adatkezelési nyilatkozat megléte és elfogadása')
    def test_data_policy(self):
        assert self.page.accept_data_policy()


@allure.epic("Felhasználó kezelés")
class TestRegistration:

    def setup_method(self):
        self.page = register.UserRegistration()

    def teardown_method(self):
        self.page.close()

    @allure.id('TC3')
    @allure.title('Új felhasználó rögzítése')
    def test_create_single_user(self):
        user_name = register.get_new_user_name(0)
        email = user_name + "@testmail.com"
        password = 'Password_01.'
        assert self.page.register_user(user_name, email, password)
        allure.dynamic.description(
            f'Felhasználónév:{user_name}, email {email},\n jelszó {password} rögzítve')

    @allure.id('TC4')
    @allure.epic("Felhasználó kezelés")
    @allure.title('10 új felhasználó rögzítése')
    def test_create_users(self):
        assert self.page.register_users_from_file()


@allure.epic("Felhasználó kezelés")
class TestLoginLogout:

    def setup_method(self):
        self.page = login.LoginUser()

    def teardown_method(self):
        self.page.close()

    @allure.id('TC5')
    @allure.title('Létező felhasználó bejelentkezése')
    @allure.description(f'A létrehozott {default_user["user_name"]} felhasználó bejelentkeztetése')
    def test_valid_user_login(self):
        assert self.page.sign_in(default_user["email"], default_user["password"], default_user["user_name"])

    @allure.id('TC6')
    @allure.title('Nem létező felhasználó bejelentkezésének visszautasítása')
    @allure.description(f'A dummy felhasználó bejelentkezésének elutasítása')
    def test_invalid_user_login(self):
        assert not database.exists_user("dummy", "dummy@dummy.com") and not self.page.sign_in("dummy@dummy.com",
                                                                                              "Password01", "dummy")

    @allure.id('TC7')
    @allure.title('Létező felhasználó kijelentkezése')
    @allure.description(f'A létrehozott {default_user["user_name"]} felhasználó kijelentkeztetése')
    def test_valid_user_logout(self):
        assert self.page.sign_in(default_user["email"], default_user["password"], default_user["user_name"])
        assert self.page.logout()


@allure.epic("Felhasználó akciók")
class TestUserActions:

    def setup_method(self):
        self.page = UserPage()

    def teardown_method(self):
        self.page.close()

    @allure.id('TC8')
    @allure.title('Cikkek listázása és mentése')
    def test_all_articles(self):
        message = ""
        result = self.page.save_article_previews(message)
        allure.dynamic.description(f"{allure_default_descriptions['TC8']}\nHibaüzenet:\n{message}")
        assert result
