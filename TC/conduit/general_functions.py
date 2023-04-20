import csv
import datetime
import json
import random
import string

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

users_data_file = "users_data.csv"
article_previews_file = "article_previews.csv"
new_articles_file = "new_articles.csv"

allure_default_descriptions = {
    "TC1": 'Oldal megnyitása és a logó megjelenésének ellenőrzése',
    "TC8": 'A felhasználó által látható összes cikk listázása és mentése'
}


def get_new_user_name(num):
    return 'testuser_' + format(num, "000") + str(datetime.datetime.now()).replace(":", "").replace("-", "").replace(
        ".", "").replace(
        " ", "")


def get_new_email(user):
    return user + "@testmail.hu"


def get_new_password(user):
    return user + "X."


def random_strings(prefix, size=5):
    return prefix.join(random.choices(string.ascii_lowercase, k=size))


def random_markdown(prefix, size=5):
    return "&gt;" + prefix.join(random.choices(string.ascii_lowercase, k=size))


def create_articles_file():
    with open(new_articles_file, 'w', encoding='UTF-8', newline='') as datafile:
        writer = csv.writer(datafile)
        title = random_strings('title')
        summary = random_strings('summary')
        body = random_strings("article", 50)
        tags = [random_strings("tag", 50) + i for i in range[3]]
        writer.writerow([title, summary, body, tags])


def create_users_file():
    with open(users_data_file, 'w', encoding='UTF-8', newline='') as datafile:
        writer = csv.writer(datafile)
        for user_id in range(10):
            user = get_new_user_name(user_id)
            email = get_new_email(user)
            password = get_new_password(user)
            writer.writerow([user_id, user, email, password])


def get_users_from_file():
    with open(users_data_file, 'r', encoding='UTF-8') as datafile:
        users = list(csv.reader(datafile))
        for user in users:
            yield user


def save_active_user(username, _email, _password):
    user_object = {
        "username": username,
        "email": _email,
        "password": _password
    }
    with open("active_user.json", "w", encoding="UTF-8", newline="") as userdata:
        userdata.write((json.dumps(user_object)))





def get_active_user():
    user_object = None
    try:
        with open("active_user.json", "r", encoding="UTF-8") as userdata:
            user_object = json.load(userdata)
    finally:
        return user_object


if __name__ == '__main__':
    active_user = get_active_user()
    if isinstance(active_user, type(None)):
        save_active_user("testuser", "testuser@testuser.hu", "Password01.")
    active_user = get_active_user()
    print(active_user)

    # create_users_file()
    # for user in get_users_from_file():
    #     user_id, user, email, password = user
    #     print(user_id, user, email, password)
