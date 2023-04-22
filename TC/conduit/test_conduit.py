import allure

import login_user as login
import main_page
import register_user as register
from article_editor import ArticleEditor
from data_layer import database
from general_functions import *
from user_data import UserData
from user_page import UserPage


@allure.epic("Alapok")
class TestMain:

    def setup_method(self):
        self.page = main_page.MainPage()

    def teardown_method(self):
        self.page.close()

    @allure.id('TC01')
    @allure.title('Conduit megjelenítése')
    @allure.description(allure_default_descriptions["TC01"])
    def test_load(self):
        assert self.page.logo().is_displayed()

    @allure.id('TC02')
    @allure.title('Conduit adatkezelési nyilatkozat')
    @allure.description(f"{allure_default_descriptions['TC02']}")
    def test_data_policy(self):
        assert self.page.accept_data_policy()


@allure.epic("Felhasználó kezelés")
class TestRegistration:

    def setup_method(self):
        self.page = register.UserRegistration()

    def teardown_method(self):
        self.page.close()

    @allure.id('TC03')
    @allure.title('Új felhasználó regisztrációja')
    def test_create_single_user(self):
        user_name = register.get_new_user_name(0)
        email = user_name + "@testmail.com"
        password = 'Password_01.'
        assert self.page.register_user(user_name, email, password)
        allure.dynamic.description(
            f'Felhasználónév:{user_name}, email {email},\n jelszó {password} rögzítve')

    @allure.id('TC04')
    @allure.epic("Felhasználó kezelés")
    @allure.title('10 új felhasználó regisztrációja')
    @allure.description(f"{allure_default_descriptions['TC04']}")
    def test_create_users(self):
        assert self.page.register_users_from_file()


@allure.epic("Felhasználó kezelés")
class TestLoginLogout:

    def setup_method(self):
        self.page = login.LoginUser(default_user)

    def teardown_method(self):
        self.page.close()

    @allure.id('TC05')
    @allure.title('Felhasználó bejelentkezése')
    @allure.description(allure_default_descriptions["TC05"])
    def test_valid_user_login(self):
        assert self.page.sign_in(default_user["email"], default_user["password"], default_user["user_name"])

    @allure.id('TC06')
    @allure.title('Nem létező felhasználó bejelentkezésének visszautasítása')
    @allure.description(allure_default_descriptions["TC06"])
    def test_invalid_user_login(self):
        assert not database.exists_user("dummy", "dummy@dummy.com") and not self.page.sign_in("dummy@dummy.com",
                                                                                              "Password01", "dummy")

    @allure.id('TC07')
    @allure.title('Létező felhasználó kijelentkezése')
    @allure.description(allure_default_descriptions["TC07"])
    def test_valid_user_logout(self):
        assert self.page.sign_in(default_user["email"], default_user["password"], default_user["user_name"])
        assert self.page.logout()


@allure.epic("Felhasználó akciók")
class TestUserActions:

    def setup_method(self):
        self.page = UserPage()

    def teardown_method(self):
        self.page.close()

    @allure.id('TC08')
    @allure.title('Cikk előnézetek listázása ')
    def test_article_previews_browse(self):
        result, message = self.page.articles_previews_browse()
        allure.dynamic.description(f"{allure_default_descriptions['TC08']}"
                                   f" Üzenet:\n{message}")
        assert result

    @allure.id('TC13')
    @allure.title('Cikk előnézetek listázása és mentése')
    def test_article_previews_save(self):
        result, message = self.page.save_article_previews()
        allure.dynamic.description(f"{allure_default_descriptions['TC13']}"
                                   f" Üzenet:\n{message}")
        assert result


@allure.epic("Felhasználó akciók")
class TestArticle:
    def setup_method(self):
        self.page = ArticleEditor()

    def teardown_method(self):
        self.page.close()

    @allure.id('TC09')
    @allure.title('Random cikk létrehozása')
    @allure.description(allure_default_descriptions["TC09"])
    def test_new_article(self):
        assert self.page.create_article()

    @allure.id('TC10')
    @allure.title('Létrehozott cikk törlése')
    @allure.description(allure_default_descriptions["TC10"])
    def test_delete_article(self):
        assert self.page.delete_article()

    @allure.id('TC11')
    @allure.title('Létrehozott cikk módosítása')
    @allure.description(allure_default_descriptions["TC11"])
    def test_edit_article(self):
        assert self.page.edit_article()


@allure.epic("Felhasználó kezelés")
class TestUserData:
    def setup_method(self):
        self.page = UserData()

    def teardown_method(self):
        self.page.close()

    @allure.id('TC12')
    @allure.title('Létrehozott felhasználó adatainak módosítása')
    @allure.description(allure_default_descriptions["TC12"])
    def test_change_user_data(self):
        new_email = get_new_email(self.page.user_name)
        new_password = get_new_password(self.page.user_name)
        assert self.page.change_user_data(self.page.user_name, new_password,
                                          f"En vagyok a default test user, e-mail címem:  {new_email}",
                                          new_email, self.page.picture)
        assert database.exists_user(self.page.user_name, new_email)
