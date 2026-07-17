from ..classes.session import Session
from .UserManager import UserManager
from .MemoryManager import MemoryManager


class SessionManager:
    """
    Responsible for creating and updating Session objects.
    """

    def __init__(
        self,
        user_manager: UserManager,
        memory_manager: MemoryManager,
    ):
        self.user_manager = user_manager
        self.memory_manager = memory_manager

    def load_session(
        self,
        user_id: str
    
    ) -> Session:
        """
        Creates a Session object for a user.
        """
        
        session_id = self.memory_manager.get_session_id(user_id) +1
        summary = self.memory_manager.get_latest_summary(user_id)

        if summary is None:
            summary = ""

        profile = self.memory_manager.get_latest_profile(user_id).to_prompt()

        messages = self.memory_manager.get_last_messages(
            user_id=user_id,
            n=10,
        )
        

        return Session(
            session_id=session_id,
            conversation_summary=summary,
            recent_messages=messages,
            profile=profile,
            
        )

    def append_message(
        self,
        session: Session,
        message,
    ) -> None:
        """
        Adds a message to the in-memory session.
        """

        session.new_messages.append(message)

        if len(session.new_messages) > 10:
            session.new_messages.pop(0)

    def update_summary(
        self,
        session: Session,
        summary: str,
    ) -> None:
        """
        Updates the cached summary.
        """

        session.summary = summary

    def update_profile(
        self,
        session: Session,
        profile,
    ) -> None:
        """
        Updates the cached profile.
        """

        session.profile = profile

    
