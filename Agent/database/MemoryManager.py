import json
import asyncio

from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    BaseMessage,
)

from Agent.classes.UserProfile import UserProfile, UserProfileSchema
from Agent.database.UserDBSchema import SQLiteDB


class MemoryManager:
    def __init__(self, db: SQLiteDB):
        self.db = db

    # =====================================================
    # Messages
    # =====================================================

    def get_session_id(self, user_id) -> int:
        self.db.cursor.execute(
            """
            SELECT session_id
            FROM messages
            WHERE user_id=?
            ORDER BY message_id DESC
            LIMIT ?
            """,
            (user_id, 1),
        )

        session_id = self.db.cursor.fetchone()
        if session_id is None:
            return 0

        return session_id[0]

    def add_message(  ## Inputs user_id ,session id and basemessages, only inserts into the database
        self,
        user_id: str,
        session_id: int,
        message: BaseMessage,
    ):

        role = "human" if isinstance(message, HumanMessage) else "ai"

        self.db.cursor.execute(
            """
            INSERT INTO messages(user_id, session_id, role, content)
            VALUES (?, ?, ?, ?)
            """,
            (
                user_id,
                session_id,
                role,
                message.content,
            ),
        )

        self.db.commit()

    def add_all_messages(self, user_id, session_id, message_list):
        for msg in message_list:
            self.add_message(user_id, session_id, msg)

    def get_last_messages(  # takes userid and no of messages input and returns the basemessage objects
        self,
        user_id: str,
        n: int,
    ) -> list[BaseMessage]:

        self.db.cursor.execute(
            """
            SELECT role, content
            FROM messages
            WHERE user_id=?
            ORDER BY message_id DESC
            LIMIT ?
            """,
            (user_id, n),
        )

        rows = self.db.cursor.fetchall()

        messages = []

        for role, content in reversed(rows):
            if role == "human":
                messages.append(HumanMessage(content))

            else:
                messages.append(AIMessage(content))

        return messages

    def get_last_msg_id(self, user_id) -> int:
        self.db.cursor.execute(
            """
            SELECT message_id
            FROM messages
            WHERE user_id = ?
            ORDER BY message_id DESC
            LIMIT 1
            """,
            (user_id,),
        )

        row = self.db.cursor.fetchone()

        message_id = row[0] if row else None

        return message_id

    def get_all_messages(  # inputs userid and returns the list of base message objects
        self,
        user_id: str,
    ) -> list[BaseMessage]:

        self.db.cursor.execute(
            """
            SELECT role, content
            FROM messages
            WHERE user_id=?
            ORDER BY message_id
            """,
            (user_id,),
        )

        rows = self.db.cursor.fetchall()

        messages = []

        for role, content in rows:
            if role == "human":
                messages.append(HumanMessage(content))

            else:
                messages.append(AIMessage(content))

        return messages

    def get_messages_after(  # inputs the message id and returns the list of  base message object
        self,
        user_id: str,
        message_id: int,
    ) -> list[BaseMessage]:

        self.db.cursor.execute(
            """
            SELECT role, content
            FROM messages
            WHERE user_id=?
            AND message_id>?
            ORDER BY message_id
            """,
            (user_id, message_id),
        )

        rows = self.db.cursor.fetchall()

        messages = []

        for role, content in rows:
            if role == "human":
                messages.append(HumanMessage(content))

            else:
                messages.append(AIMessage(content))

        return messages

    def delete_last_messages(  # inputs user  id and number of messages to delete.
        self,
        user_id: str,
        n: int,
    ):

        self.db.cursor.execute(
            """
            DELETE FROM messages
            WHERE message_id IN (
                SELECT message_id
                FROM messages
                WHERE user_id=?
                ORDER BY message_id DESC
                LIMIT ?
            )
            """,
            (user_id, n),
        )

        self.db.commit()

    def delete_all_messages(  # inputs user id and truncates all messages.
        self,
        user_id: str,
    ):

        self.db.cursor.execute(
            """
            DELETE FROM messages
            WHERE user_id=?
            """,
            (user_id,),
        )

        self.db.commit()

    # =====================================================
    # Summary
    # =====================================================

    def save_summary(  # inputs str summary and used id
        self,
        user_id: str,
        summary: str,
    ):

        self.db.cursor.execute(
            """
            INSERT INTO summaries(user_id, summary)
            VALUES (?, ?)
            """,
            (user_id, summary),
        )

        self.db.commit()

    def get_latest_summary(
        self,
        user_id: str,
    ) -> list[HumanMessage] | None:

        self.db.cursor.execute(
            """
            SELECT summary
            FROM summaries
            WHERE user_id = ?
            ORDER BY summary_id DESC
            LIMIT 5
            """,
            (user_id,),
        )

        rows = self.db.cursor.fetchmany(5)

        if not rows:
            return list()

        summary_list = []

        for row in rows:
            summary_list.append(HumanMessage(content=row[0]))

        return summary_list

    def delete_summary(
        self,
        summary_id: int,
    ):
        self.db.cursor.execute(
            """
        DELETE FROM summaries
        WHERE summary_id = ?
        """,
            (summary_id,),
        )

        self.db.commit()

    def delete_latest_summary(
        self,
        user_id: str,
    ):
        self.db.cursor.execute(
            """
        DELETE FROM summaries
        WHERE summary_id = (
            SELECT summary_id
            FROM summaries
            WHERE user_id = ?
            ORDER BY summary_id DESC
            LIMIT 1
        )
        """,
            (user_id,),
        )

        self.db.commit()

    def delete_all_summaries(
        self,
        user_id: str,
    ):
        self.db.cursor.execute(
            """
        DELETE FROM summaries
        WHERE user_id = ?
        """,
            (user_id,),
        )

        self.db.commit()

    # =====================================================
    # Profile
    # =====================================================

    def save_profile(  # inputs userid and profile and converts dict into string and saves in db
        self,
        user_id: str,
        profile: UserProfile,
    ):

        self.db.cursor.execute(
            """
            INSERT INTO profiles(user_id, profile)
            VALUES (?, ?)
            """,
            (
                user_id,
                json.dumps(profile.to_dict()),
            ),
        )

        self.db.commit()

    def get_latest_profile(  # converts string into python object and returns the object
        self,
        user_id: str,
    ) -> UserProfile | None:

        self.db.cursor.execute(
            """
            SELECT profile
            FROM profiles
            WHERE user_id=?
            ORDER BY profile_id DESC
            LIMIT 1
            """,
            (user_id,),
        )

        row = self.db.cursor.fetchone()

        if row is None:
            return UserProfile()
        return UserProfile.from_dict(json.loads(row[0]))

    def delete_profile(
        self,
        profile_id: int,
    ):
        self.db.cursor.execute(
            """
        DELETE FROM profiles
        WHERE profile_id = ?
        """,
            (profile_id,),
        )

        self.db.commit()

    def delete_all_profiles(
        self,
        user_id: str,
    ):
        self.db.cursor.execute(
            """
        DELETE FROM profiles
        WHERE user_id = ?
        """,
            (user_id,),
        )

        self.db.commit()

    def delete_latest_profile(
        self,
        user_id: str,
    ):
        self.db.cursor.execute(
            """
        DELETE FROM profiles
        WHERE profile_id = (
            SELECT profile_id
            FROM profiles
            WHERE user_id = ?
            ORDER BY profile_id DESC
            LIMIT 1
        )
        """,
            (user_id,),
        )

        self.db.commit()

    # =====================================================
    # Tracker
    # =====================================================

    def get_summary_track(self, user_id: str) -> int:

        self.db.cursor.execute(
            """
            SELECT summary_message_id
            FROM memory_tracker
            WHERE user_id=?
            """,
            (user_id,),
        )

        row = self.db.cursor.fetchone()

        return 0 if row is None else row[0]

    def update_summary_track(
        self,
        user_id: str,
        message_id: int,
    ):

        self.db.cursor.execute(
            """
            UPDATE memory_tracker
            SET summary_message_id=?
            WHERE user_id=?
            """,
            (
                message_id,
                user_id,
            ),
        )

        self.db.commit()

    def get_profile_track(self, user_id: str) -> int:

        self.db.cursor.execute(
            """
            SELECT profile_message_id
            FROM memory_tracker
            WHERE user_id=?
            """,
            (user_id,),
        )

        row = self.db.cursor.fetchone()

        return 0 if row is None else row[0]

    def update_profile_track(
        self,
        user_id: str,
        message_id: int,
    ):

        self.db.cursor.execute(
            """
            UPDATE memory_tracker
            SET profile_message_id=?
            WHERE user_id=?
            """,
            (
                message_id,
                user_id,
            ),
        )

        self.db.commit()
