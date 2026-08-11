import json

from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    BaseMessage,
)

from Agent.classes.UserProfile import UserProfileSchema


class Serializer:
    """
    Utility class for converting between Python objects
    and database-compatible representations.
    """

    # =====================================================
    # Messages
    # =====================================================

    @staticmethod
    def message_to_db(message: BaseMessage) -> tuple[str, str]:
        """
        Converts a LangChain message into
        (role, content).
        """

        if isinstance(message, HumanMessage):
            return "human", message.content

        if isinstance(message, AIMessage):
            return "ai", message.content

        raise ValueError(f"Unsupported message type: {type(message)}")

    @staticmethod
    def db_to_message(
        role: str,
        content: str,
    ) -> BaseMessage:
        """
        Converts a database row back into
        a LangChain message.
        """

        if role == "human":
            return HumanMessage(content=content)

        if role == "ai":
            return AIMessage(content=content)

        raise ValueError(f"Unknown role: {role}")

    @staticmethod
    def rows_to_messages(rows: list[tuple[str, str]]) -> list[BaseMessage]:
        """
        Converts multiple database rows into
        LangChain messages.
        """

        return [Serializer.db_to_message(role, content) for role, content in rows]

    # =====================================================
    # Profile
    # =====================================================

    @staticmethod
    def profile_to_db(
        profile: UserProfileSchema,
    ) -> str:
        """
        Converts a UserProfileSchema into a JSON string.
        """

        return json.dumps(profile.profile_json())

    @staticmethod
    def db_to_profile(
        profile_json: str,
    ) -> UserProfileSchema:
        """
        Converts a JSON string back into
        a UserProfileSchema.
        """

        return UserProfileSchema.model_validate(json.loads(profile_json))
