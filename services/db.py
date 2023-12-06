import psycopg2

import config

keepalive_kwargs = {
    "keepalives": 1,
    "keepalives_idle": 60,
    "keepalives_interval": 10,
    "keepalives_count": 5
}


class DataBase:

    def __init__(self):
        self.connect = psycopg2.connect(config.db_auth, **keepalive_kwargs)
        self.cursor = self.connect.cursor()

    async def add_users(self, user_id, user_name, user_username):
        with self.connect:
            self.cursor.execute(
                """INSERT INTO users (user_id, user_name, user_username) 
                   VALUES (%s, %s, %s) ON CONFLICT DO NOTHING""",
                (user_id, user_name, user_username)
            )

    async def delete_user(self, user_id):
        with self.connect:
            self.cursor.execute(
                "DELETE FROM users WHERE user_id = %s;",
                (user_id,))

    async def user_exist(self, user_id):
        with self.connect:
            self.cursor.execute("""SELECT * FROM users WHERE user_id = %s""", (user_id,))
            return self.cursor.fetchall()

    async def get_language(self, user_id):
        with self.connect:
            self.cursor.execute("SELECT DISTINCT language FROM users WHERE user_id = %s", (user_id,))
            return self.cursor.fetchone()[0]

    async def get_notes(self, user_id):
        with self.connect:
            self.cursor.execute('SELECT id, note FROM notes WHERE user_id = %s', (user_id,))
            return self.cursor.fetchall()

    async def get_note(self, note_id):
        with self.connect:
            self.cursor.execute('SELECT note FROM notes WHERE id = %s', (note_id,))
            return self.cursor.fetchone()

    async def delete_note(self, note_id):
        with self.connect:
            self.cursor.execute('DELETE FROM notes WHERE id = %s', (note_id,))

    async def add_note(self, user_id, note_text):
        with self.connect:
            self.cursor.execute('INSERT INTO notes (user_id, note) VALUES (%s, %s)', (user_id, note_text))

    async def set_language(self, user_id, language):
        with self.connect:
            self.cursor.execute("UPDATE users SET language=%s WHERE user_id=%s", (language, user_id))

    async def user_count(self):
        with self.connect:
            self.cursor.execute("SELECT COUNT(*) FROM users")
            return self.cursor.fetchone()[0]

    async def status(self, user_id):
        with self.connect:
            self.cursor.execute("SELECT DISTINCT status FROM users WHERE user_id = %s", (user_id,))
            return self.cursor.fetchone()[0]

    async def get_admins(self):
        with self.connect:
            self.cursor.execute("SELECT DISTINCT user_id FROM users WHERE status = 'admin'")
            return self.cursor.fetchall()

    async def all_users(self):
        with self.connect:
            self.cursor.execute("SELECT user_id FROM users")
            return self.cursor.fetchall()

    async def user_update_name(self, user_id, user_name, user_username):
        with self.connect:
            self.cursor.execute("UPDATE users SET user_username=%s, user_name=%s WHERE user_id=%s",
                                (user_username, user_name, user_id))

    async def get_user_info(self, user_id):
        with self.connect:
            self.cursor.execute(
                "SELECT user_name, user_username, status FROM users WHERE user_id = %s", (user_id,))
            return self.cursor.fetchone()

    async def get_user_info_username(self, user_username):
        with self.connect:
            self.cursor.execute(
                "SELECT user_name, user_id, status FROM users WHERE user_username = %s", (user_username,))
            return self.cursor.fetchone()

    async def ban_user(self, user_id):
        with self.connect:
            self.cursor.execute("UPDATE users SET status=%s WHERE user_id=%s", ("ban", user_id))

    async def get_all_users_info(self):
        with self.connect:
            self.cursor.execute(
                "SELECT user_id, user_name, user_username, language, status FROM users")
            return self.cursor.fetchall()

    async def unban_user(self, user_id):
        with self.connect:
            self.cursor.execute("UPDATE users SET status=%s WHERE user_id=%s", ("user", user_id))
