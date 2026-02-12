import os
from src.services.llm.gemini_provider import GeminiLLM
from src.services.llm.ollama_provider import OllamaLLM
from src.services.database.postgres_provider import PostgresDatabase
from src.services.database.vector_provider import PostgresVectorStore

# Scraper Imports
from src.services.scrapper.providers.unstop_provider import UnstopScraper
from src.services.scrapper.providers.linkedin import LinkedInProvider
from src.services.scrapper.providers.local_provider import LocalScraper

# Interface Imports
from src.services.interfaces.LLMProvider import LLMProvider
from src.services.interfaces.DatabaseProvider import DatabaseProvider
from src.services.interfaces.ScraperProvider import ScraperProvider
from src.services.interfaces.VectorStoreProvider import VectorStoreProvider 

class ServiceContainer:
    _llm_instance = None
    _db_instance = None
    _vector_instance = None

    # Registry including both Gemini and Ollama
    _LLM_REGISTRY = { 
        "gemini": GeminiLLM,
        "ollama": OllamaLLM 
    }
    
    _DB_REGISTRY = { "postgres": PostgresDatabase }
    
    _SCRAPER_REGISTRY = { 
        "unstop": UnstopScraper,
        "linkedin": LinkedInProvider,
        "local": LocalScraper
    }    
    
    _VECTOR_REGISTRY = { "postgres": PostgresVectorStore }

    @staticmethod
    def get_llm() -> LLMProvider:
        if ServiceContainer._llm_instance is None:
            # Default to ollama if not specified to avoid quota errors
            llm_type = os.getenv("LLM_TYPE", "ollama").lower()
            provider_cls = ServiceContainer._LLM_REGISTRY.get(llm_type, OllamaLLM)
            ServiceContainer._llm_instance = provider_cls()
        return ServiceContainer._llm_instance

    @staticmethod
    def get_database() -> DatabaseProvider:
        if ServiceContainer._db_instance is None:
            db_type = os.getenv("DB_TYPE", "postgres").lower()
            ServiceContainer._db_instance = ServiceContainer._DB_REGISTRY[db_type]()
        return ServiceContainer._db_instance

    @staticmethod
    def get_vector_store() -> VectorStoreProvider:
        if ServiceContainer._vector_instance is None:
            vector_type = os.getenv("VECTOR_TYPE", "postgres").lower()
            provider_cls = ServiceContainer._VECTOR_REGISTRY.get(vector_type, PostgresVectorStore)
            ServiceContainer._vector_instance = provider_cls()
        return ServiceContainer._vector_instance

    @staticmethod
    def get_scraper(platform: str, driver) -> ScraperProvider:
        platform_key = platform.lower().strip()
        for key, provider_cls in ServiceContainer._SCRAPER_REGISTRY.items():
            if key in platform_key:
                return provider_cls(driver)
        raise ValueError(f"No scraper found for '{platform}'")