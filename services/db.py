import sqlite3


class DataBase:

    def __init__(self, db_file):
        self.connect = sqlite3.connect(db_file)
        self.cursor = self.connect.cursor()

    async def add_users(self, user_id, user_name, user_username):
        with self.connect:
            return self.cursor.execute(
                """INSERT OR IGNORE INTO users (user_id, user_name, user_username) VALUES (?, ?, ?)""",
                (user_id, user_name, user_username))

    async def user_exist(self, user_id):
        with self.connect:
            return self.cursor.execute("""SELECT * FROM users WHERE user_id = (?)""", (user_id,)).fetchall()

    async def get_language(self, user_id):
        with self.connect:
            return self.cursor.execute("SELECT DISTINCT language FROM users WHERE user_id=(?)",
                                       (user_id,)).fetchone()[0]

    async def get_notes(self, user_id):
        with self.connect:
            return self.cursor.execute('SELECT id, note FROM notes WHERE user_id = ?', (user_id,)).fetchall()

    async def get_note(self, note_id):
        with self.connect:
            return self.cursor.execute('SELECT note FROM notes WHERE id = ?', (note_id,)).fetchone()

    async def delete_note(self, note_id):
        with self.connect:
            return self.cursor.execute('DELETE FROM notes WHERE id = ?', (note_id,))

    async def add_note(self, user_id, note_text):
        with self.connect:
            return self.cursor.execute('INSERT INTO notes (user_id, note) VALUES (?, ?)', (user_id, note_text))

    async def set_language(self, user_id, language):
        with self.connect:
            return self.cursor.execute("UPDATE users SET language=(?) WHERE user_id=(?)", (language, user_id))

    async def user_count(self):
        with self.connect:
            return self.cursor.execute("SELECT COUNT(*) FROM users").fetchone()[0]

    async def status(self, user_id):
        with self.connect:
            return self.cursor.execute("SELECT DISTINCT status FROM users WHERE user_id = (?)", (user_id,)).fetchone()[
                0]

    async def get_admins(self):
        with self.connect:
            return self.cursor.execute("SELECT DISTINCT user_id FROM users WHERE status = admin", ).fetchall()

    async def all_users(self):
        with self.connect:
            return self.cursor.execute("SELECT user_id FROM users").fetchall()

    async def user_update_name(self, user_id, user_name, user_username):
        with self.connect:
            return self.cursor.execute("UPDATE users SET user_username=(?), user_name=(?) WHERE user_id=(?)",
                                       (user_username, user_name, user_id,))

    async def get_user_info(self, user_id):
        with self.connect:
            return self.cursor.execute(
                "SELECT user_name, user_username, status FROM users WHERE user_id = (?)",
                (user_id,))

    async def get_user_info_username(self, user_username):
        with self.connect:
            return self.cursor.execute(
                "SELECT user_name, user_id, status FROM users WHERE user_username = (?)",
                (user_username,))

    async def ban_user(self, user_id):
        with self.connect:
            return self.cursor.execute("UPDATE users SET status=(?) WHERE user_id=(?)", ("ban", user_id))

    async def get_all_users_info(self):
        with self.connect:
            return self.cursor.execute(
                "SELECT user_id, user_name, user_username, language, status FROM users").fetchall()

    async def unban_user(self, user_id):
        with self.connect:
            return self.cursor.execute("UPDATE users SET status=(?) WHERE user_id=(?)", ("user", user_id))
