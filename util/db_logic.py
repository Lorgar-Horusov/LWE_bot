import sqlite3
import datetime

class AchievementsDataBase:
    def __init__(self, db_path='LWE_DB'):
        self.db_path = db_path
        self._initialize_db()

    def _initialize_db(self):

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS achievements
            (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                achievement TEXT NOT NULL,
                description TEXT,
                server_id TEXT NOT NULL
            )
            '''
            )
            conn.commit()

    def add_achievement(self, user_id, achievement, description, server_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO achievements (user_id, achievement, description, server_id) VALUES (?, ?, ?, ?)",
                           (user_id, achievement, description, server_id))
            conn.commit()

    def get_achievements(self, user_id, server_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT achievement FROM achievements WHERE user_id = ? AND server_id = ?", (user_id, server_id))
            return cursor.fetchall()

    def clear_achievements(self, user_id, server_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM achievements WHERE user_id = ? AND server_id = ?", (user_id, server_id))
            conn.commit()

    def remove_achievement(self, user_id, achievement, server_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM achievements WHERE user_id = ? AND achievement = ? AND server_id = ?", (user_id, achievement, server_id))
            conn.commit()


class ModerationDatabase:
    def __init__(self, db_path='LWE_DB'):
        self.db_path = db_path
        self._initialize_db()

    def _initialize_db(self):

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS warns
            (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                reason TEXT NOT NULL,
                warn_date TEXT NOT NULL,
                server_id TEXT NOT NULL
            )
            '''
            )
            conn.commit()
    def add_warn(self, user_id, reason, server_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO warns (user_id, reason, warn_date, server_id) VALUES (?, ?, ?, ?)",
                           (user_id, reason, datetime.datetime.now().strftime('%d-%m-%Y'), server_id))
            conn.commit()

    def get_warns(self, user_id, server_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, reason, warn_date FROM warns WHERE user_id = ? AND server_id = ?", (user_id, server_id))
            return cursor.fetchall()

    def delete_warn(self, user_id, server_id, warn_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM warns WHERE user_id = ? AND server_id = ? AND id = ?", (user_id, server_id, warn_id))
            conn.commit()

class ChatLogger:
    def __init__(self, db_path='LWE_DB', max_records=50, retention_days=14):
        self.db_path = db_path
        self.max_records = max_records
        self.retention_days = retention_days
        self._initialize_db()

    def _initialize_db(self):

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                   CREATE TABLE IF NOT EXISTS deleted_messages
                    (
                        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        autor TEXT NOT NULL,
                        message TEXT,
                        deletion_data TEXT NOT NULL,
                        server_id INTEGER NOT NULL 
                    )
              ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS edited_messages
                (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    autor TEXT NOT NULL,
                    original_message TEXT NOT NULL,
                    edited_message TEXT NOT NULL,
                    edited_date TEXT NOT NULL,
                    server_id INTEGER NOT NULL 
                )
            ''')
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS warns
            (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                reason TEXT NOT NULL,
                warn_date TEXT NOT NULL,
                server_id INTEGER NOT NULL
            )
            '''
            )
            conn.commit()

    def _check_and_delete_old_log(self, table_name):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            if count >= self.max_records:
                cursor.execute(f"SELECT id, deletion_data FROM {table_name} ORDER BY deletion_data LIMIT 1")
                old_records = cursor.fetchone()
                if old_records:
                    oldest_id, oldest_data = old_records
                    oldest_data = datetime.datetime.strptime(oldest_data, '%d-%m-%Y').date()
                    expiration_data = datetime.datetime.now().date() - datetime.timedelta(days=self.retention_days)
                    if oldest_data < expiration_data:
                        cursor.execute(f"DELETE FROM {table_name} WHERE id = ?", (oldest_id,))
                        conn.commit()

    def message_deletion_logger(self, autor, message, server_id):
        try:
            self._check_and_delete_old_log('deleted_messages')
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO deleted_messages (autor, message, deletion_data, server_id) VALUES (?, ?, ?, ?)",
                               (autor, message, datetime.datetime.now().strftime('%d-%m-%Y'), server_id))
                conn.commit()
                print('Log saved')
        except Exception as e:
            print(f'Error in message_deletion_logger: {e}')

    def message_edition_logger(self, autor, original_message, edited_message, server_id):
        try:
            self._check_and_delete_old_log('edited_messages')
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO edited_messages (autor, original_message, edited_message, edited_date, server_id) VALUES (?, ?, ?, ?, ?)",
                               (autor, original_message, edited_message, datetime.datetime.now().strftime('%d-%m-%Y'), server_id))
                conn.commit()
                print('Log saved')
        except Exception as e:
            print(f'Error in message_edition_logger: {e}')

    def get_logs(self, table_name, server_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table_name} WHERE server_id = ?", (server_id, ))
            return cursor.fetchall()


if __name__ == '__main__':
    logger = ModerationDatabase()