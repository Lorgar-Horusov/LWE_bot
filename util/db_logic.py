import sqlite3
import datetime


class ChatLogger():
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
        self._check_and_delete_old_log('Deleted_messages')
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO deleted_messages (autor, message, deletion_data, server_id) VALUES (?, ?, ?, ?)",
                           (autor, message, datetime.datetime.now().strftime('%d-%m-%Y'), server_id))
            conn.commit()

    def message_edition_logger(self, autor, original_message, edited_message, server_id):
        self._check_and_delete_old_log('Edited_messages')
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO edited_messages (autor, original_message, edited_message, edited_date, server_id) VALUES (?, ?, ?, ?, ?)",
                           (autor, original_message, edited_message, datetime.datetime.now().strftime('%d-%m-%Y'), server_id))
            conn.commit()

    def get_logs(self, table_name, server_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table_name} WHERE server_id = ?", (server_id, ))
            return cursor.fetchall()


if __name__ == '__main__':
    logger = ChatLogger()
    logger.message_deletion_logger('Lorgar', 'This is deleted message', 1)
    logger.message_edition_logger('Lorgar', 'Original', 'Edited', 1)
    print(logger.get_logs('deleted_messages', 1))
    print(logger.get_logs('edited_messages', 1))