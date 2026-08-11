from dataclasses import dataclass, field

from langchain_core.messages import BaseMessage

from Agent.classes.UserProfile import UserProfile


@dataclass
class Session:
    """
    Represents the current conversation context for a user.
    """

    session_id: int
    conversation_summary: str
    recent_messages: list[BaseMessage] = field(default_factory=list)
    new_messages: list[BaseMessage] = field(default_factory=list)
    profile: UserProfile | None = None
