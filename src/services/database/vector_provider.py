import os
from src.services.interfaces.VectorStoreProvider import VectorStoreProvider
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector
from dotenv import load_dotenv

load_dotenv()

class PostgresVectorStore(VectorStoreProvider):
    def __init__(self):
        self.db_uri = os.getenv("DB_URI")
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.db_uri: raise ValueError("Missing DB_URI")
        if not self.api_key: raise ValueError("Missing GOOGLE_API_KEY")
        
        # Initialize Embeddings
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=self.api_key
        )
        
        # Initialize PGVector
        self.store = PGVector(
            embeddings=self.embeddings,
            collection_name="resume_embeddings",
            connection=self.db_uri,
            use_jsonb=True
        )

    def add_documents(self, documents):
        self.store.add_documents(documents)

    def as_retriever(self, search_kwargs=None):
        if search_kwargs is None: search_kwargs = {}
        return self.store.as_retriever(search_kwargs=search_kwargs)