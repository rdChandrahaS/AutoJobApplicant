from abc import ABC, abstractmethod

class BaseScraper(ABC):
    def __init__(self, driver):
        self.driver = driver

    @abstractmethod
    def login(self, username, password):
        pass

    @abstractmethod
    def search_jobs(self, query):
        pass