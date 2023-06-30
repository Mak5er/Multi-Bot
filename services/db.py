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
