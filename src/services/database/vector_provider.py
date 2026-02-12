import os
from langchain_postgres.vectorstores import PGVector
from langchain_ollama import OllamaEmbeddings
from src.services.interfaces.VectorStoreProvider import VectorStoreProvider

class PostgresVectorStore(VectorStoreProvider):
    def __init__(self):
        self.connection_string = os.getenv("DB_URI")
        self.collection_name = "resume_embeddings"
        
        # FIX: Switched from GeminiEmbeddings to OllamaEmbeddings
        # Ensure you have run: ollama pull nomic-embed-text
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")
        
        self.store = PGVector(
            embeddings=self.embeddings,
            collection_name=self.collection_name,
            connection=self.connection_string,
            use_jsonb=True,
        )

    def add_documents(self, documents):
        self.store.add_documents(documents)

    def similarity_search(self, query: str, k: int = 4):
        return self.store.similarity_search(query, k=k)