from abc import ABC, abstractmethod

class BaseScraper(ABC):
    @abstractmethod
    def extract_form_fields(self, url: str) -> list:
        """Finds inputs, textareas, and labels."""
        pass

    @abstractmethod
    def submit_application(self, url: str, validated_data: dict) -> bool:
        """Injects data into the site and clicks apply."""
        pass