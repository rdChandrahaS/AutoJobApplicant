from abc import ABC, abstractmethod
from typing import Any, List

class VectorStoreProvider(ABC):
    """
    Abstract Base Class for Vector Databases (Postgres, Pinecone, Chroma).
    """
    
    @abstractmethod
    def add_documents(self, documents: List[Any]):
        """Adds text chunks to the vector database."""
        pass

    @abstractmethod
    def as_retriever(self, search_kwargs: dict = None) -> Any:
        """Returns a retriever object for LangChain."""
        pass