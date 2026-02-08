from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class DatabaseProvider(ABC):
    """
    Abstract Base Class for any Database (Postgres, SQLite, MongoDB)
    """
    @abstractmethod
    def add_user_message(self, session_id: str, message: str):
        pass

    @abstractmethod
    def add_ai_message(self, session_id: str, message: str):
        pass

    @abstractmethod
    def get_history(self, session_id: str) -> Any:
        pass

    @abstractmethod
    def save_session_title(self, session_id: str, title: str):
        pass
    
    @abstractmethod
    def get_all_sessions(self) -> List[Dict[str, str]]:
        pass
    
    @abstractmethod
    def delete_session(self, session_id: str):
        pass