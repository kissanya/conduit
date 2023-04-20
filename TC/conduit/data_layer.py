import psycopg2
from register_user import UserRegistration


class ConduitDatabase:
    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
        except psycopg2.Error as e:
            print("Error connecting to database:", e)

    def execute_query(self, query):
        try:
            cur = self.conn.cursor()
            cur.execute(query)
            result = cur.fetchall()
            cur.close()
            return result
        except psycopg2.Error as e:
            print("Error executing query:", e)

    def exists_user(self, user_name, email):
        self.connect()
        result = self.execute_query(
            f"SELECT username, password, email FROM users WHERE username ='{user_name}' and email = '{email}'")
        self.close()
        if len(list(result)) == 1:
            return True
        else:
            return False

    def close(self):
        self.conn.close()


database = ConduitDatabase('realworld', "user", "userpassword", "localhost", "54320")


def register_user(user, email, password):
    if not database.exists_user(user, email):
        user_registration = UserRegistration()
        assert user_registration.register_user(user, email, password)
        user_registration.close()


if __name__ == '__main__':
    register_user("tesztelek", "tesztelek@tesztelek.hu", "Password01.")
    print(database.exists_user("user32", "user32@mail.com"))
    print(database.exists_user("tesztelek", "tesztelek@tesztelek.hu"))
