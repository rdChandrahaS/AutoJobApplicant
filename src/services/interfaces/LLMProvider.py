from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class LLMProvider(ABC):
    """
    Abstract Base Class for any AI Model (Gemini, OpenAI, Claude, etc.)
    """
    @abstractmethod
    def generate(self, messages: List[Any], streaming: bool = False, config: Optional[Dict] = None) -> str:
        pass

    @abstractmethod
    def invoke(self, messages: List[Any], config: Optional[Dict] = None) -> Any:
        pass
    
    @abstractmethod
    def bind_tools(self, tools: List[Any]) -> Any:
        pass