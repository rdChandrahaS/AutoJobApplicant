import os
from src.services.llm.gemini_provider import GeminiLLM
from src.services.database.postgres_provider import PostgresDatabase
from src.services.scrapper.providers.unstop_provider import UnstopScraper
from src.services.database.vector_provider import PostgresVectorStore

from src.services.interfaces.LLMProvider import LLMProvider
from src.services.interfaces.DatabaseProvider import DatabaseProvider
from src.services.interfaces.ScraperProvider import ScraperProvider
from src.services.interfaces.VectorStoreProvider import VectorStoreProvider 

class ServiceContainer:
    """
    Dependency Injection Container (Registry Pattern).
    """
    
    _llm_instance = None
    _db_instance = None
    _vector_instance = None # <--- NEW SINGLETON

    _LLM_REGISTRY = { "gemini": GeminiLLM }
    _DB_REGISTRY = { "postgres": PostgresDatabase }
    _SCRAPER_REGISTRY = { "unstop": UnstopScraper }
    _VECTOR_REGISTRY = { "postgres": PostgresVectorStore } # <--- NEW REGISTRY

    @staticmethod
    def get_llm() -> LLMProvider:
        if ServiceContainer._llm_instance is None:
            llm_type = os.getenv("LLM_TYPE", "gemini").lower()
            ServiceContainer._llm_instance = ServiceContainer._LLM_REGISTRY[llm_type]()
        return ServiceContainer._llm_instance

    @staticmethod
    def get_database() -> DatabaseProvider:
        if ServiceContainer._db_instance is None:
            db_type = os.getenv("DB_TYPE", "postgres").lower()
            ServiceContainer._db_instance = ServiceContainer._DB_REGISTRY[db_type]()
        return ServiceContainer._db_instance

    @staticmethod
    def get_vector_store() -> VectorStoreProvider: # <--- NEW METHOD
        if ServiceContainer._vector_instance is None:
            # You can add VECTOR_TYPE to .env if you want dynamic switching
            vector_type = os.getenv("VECTOR_TYPE", "postgres").lower()
            
            provider_cls = ServiceContainer._VECTOR_REGISTRY.get(vector_type)
            if not provider_cls:
                 raise ValueError(f"Unknown VECTOR_TYPE: '{vector_type}'")
            
            ServiceContainer._vector_instance = provider_cls()
        return ServiceContainer._vector_instance

    @staticmethod
    def get_scraper(platform: str, driver) -> ScraperProvider:
        platform_key = platform.lower().strip()
        for key, provider_cls in ServiceContainer._SCRAPER_REGISTRY.items():
            if key in platform_key:
                return provider_cls(driver)
        raise ValueError(f"No scraper found for '{platform}'")