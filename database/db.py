import psycopg2
from config_data.config import Config


class DataBase:
    def __init__(self, dbconfig: Config):
        self.conn = psycopg2.connect(
            host=dbconfig.db.db_host,
            dbname=dbconfig.db.database,
            user=dbconfig.db.db_user,
            password=dbconfig.db.db_password
        )

    def existsUser(self, user_id):
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute("SELECT id FROM users WHERE user_id = %s", (user_id,))
                flag = bool(len(cur.fetchall()))
        return flag

    def addUser(self, user_id, first_name, last_name):
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute("INSERT INTO users (user_id, first_name, last_name)  VALUES (%s, %s, %s)",
                            (user_id, first_name, last_name))

    def delUser(self, user_id):
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute("DELETE FROM users WHERE user_id = %s", (user_id,))

    def close(self):
        self.conn.close()
