import csv
import datetime

users_data="users_data.csv"
def get_new_user_name(num):
    return 'testuser_' + format(num, "000") + str(datetime.datetime.now()).replace(":", "").replace("-", "").replace(
        ".", "").replace(
        " ", "")


def get_new_email(user):
    return user + "@testmail.hu"


def get_new_password(user):
    return user + "X."


def create_users_file():
    with open(users_data, 'w', encoding='UTF-8', newline='') as datafile:
        writer = csv.writer(datafile)
        for user_id in range(10):
            user = get_new_user_name(user_id)
            email = get_new_email(user)
            password = get_new_password(user)
            writer.writerow([user_id, user, email, password])


def get_users_from_file():
    with open(users_data, 'r', encoding='UTF-8') as datafile:
        users = list(csv.reader(datafile))
        for user in users:
            yield user


if __name__ == '__main__':
    create_users_file()
    for user in get_users_from_file():
        user_id, user, email, password = user
        print(user_id, user, email, password)
