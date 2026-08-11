from Agent.database.UserDBSchema import SQLiteDB


class UserManager:
    """
    CRUD operations for users.
    """

    def __init__(self, db: SQLiteDB):
        self.db = db

    def create_user(self, user_id: str) -> bool:
        """
        Creates a new user.

        Returns True if created.
        Returns False if already exists.
        """

        if self.user_exists(user_id):
            return False

        self.db.cursor.execute(
            """
            INSERT INTO users(user_id)
            VALUES(?)
            """,
            (user_id,),
        )
        self.db.cursor.execute(
            """
            INSERT INTO memory_tracker(user_id)
            VALUES (?)
            """,
            (user_id,),
        )
        self.db.commit()

        print("Created New user")
        return True

    def delete_user(self, user_id: str) -> bool:
        """
        Deletes a user and all associated data.

        Returns True if deleted.
        """

        self.db.cursor.execute(
            """
            DELETE FROM users
            WHERE user_id = ?
            """,
            (user_id,),
        )

        deleted = self.db.cursor.rowcount

        self.db.commit()

        return deleted > 0

    def user_exists(self, user_id: str) -> bool:
        """
        Returns True if user exists.
        """

        self.db.cursor.execute(
            """
            SELECT 1
            FROM users
            WHERE user_id = ?
            """,
            (user_id,),
        )

        return self.db.cursor.fetchone() is not None

    def get_all_users(self) -> list[str]:
        """
        Returns list of all user ids.
        """

        self.db.cursor.execute(
            """
            SELECT user_id
            FROM users
            """
        )

        return [row[0] for row in self.db.cursor.fetchall()]

    def delete_all_users(self):
        users = self.get_all_users()

        for u in users:
            self.delete_user(u)
