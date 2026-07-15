import sqlite3
from ..config import DATABASE_DIR


class SQLiteDB:
    """
    SQLite database manager.
    Responsible only for database connection and table management.
    """

    def __init__(self, db_path: str = "database.db"):
        
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
                user_id TEXT PRIMARY KEY
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages(
                message_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                session_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,

                FOREIGN KEY(user_id)
                    REFERENCES users(user_id)
                    ON DELETE CASCADE
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS summaries(
                summary_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                summary TEXT NOT NULL,

                FOREIGN KEY(user_id)
                    REFERENCES users(user_id)
                    ON DELETE CASCADE
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS profiles(
                profile_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                profile TEXT NOT NULL,

                FOREIGN KEY(user_id)
                    REFERENCES users(user_id)
                    ON DELETE CASCADE
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS memory_tracker(
                user_id TEXT PRIMARY KEY,
                summary_message_id INTEGER DEFAULT 0,
                profile_message_id INTEGER DEFAULT 0,

                FOREIGN KEY(user_id)
                    REFERENCES users(user_id)
                    ON DELETE CASCADE
            )
        """)

        self.conn.commit()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()

    def clear_database(self):
        self.cursor.execute("DELETE FROM messages")
        self.cursor.execute("DELETE FROM summaries")
        self.cursor.execute("DELETE FROM profiles")
        self.cursor.execute("DELETE FROM memory_tracker")
        self.cursor.execute("DELETE FROM users")

        self.conn.commit()

    def reset_database(self):
        self.cursor.execute("DROP TABLE IF EXISTS messages")
        self.cursor.execute("DROP TABLE IF EXISTS summaries")
        self.cursor.execute("DROP TABLE IF EXISTS profiles")
        self.cursor.execute("DROP TABLE IF EXISTS memory_tracker")
        self.cursor.execute("DROP TABLE IF EXISTS users")

        self.conn.commit()

        self.create_tables()