from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class ScraperProvider(ABC):
    """
    Abstract Base Class for Job Platforms (Unstop, LinkedIn, Indeed)
    """
    def __init__(self, driver):
        self.driver = driver

    @abstractmethod
    def login(self, username, password) -> tuple[bool, str]:
        pass

    @abstractmethod
    def search_jobs(self, query) -> tuple[bool, str]:
        pass