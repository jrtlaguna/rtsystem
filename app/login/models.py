from werkzeug.security import check_password_hash
from app import get_db_connection, login_manager

@login_manager.user_loader
def load_user(username):
    return User(username)

class User(object):
    def __init__(self, username = None):
        self.username  = None
        self.password_hash = None
        self.is_active = False
        self.is_authenticated = True
        self.account_type = None

        if username:
            self.username = username
            self.__load_user()


    def __load_user(self):
        connection = get_db_connection()

        try:
            with connection.cursor() as cursor:
                sql = 'SELECT username, password, isActive, accountType FROM account WHERE username=%s'
                cursor.execute(sql, self.username)

                result = cursor.fetchone()
                if result:
                    self.username, self.password_hash, self.is_active, self.account_type = result
                else:
                    self.username = None

        finally:
            connection.close()


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    def get_id(self):
        return self.username