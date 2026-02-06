
from providers.linkedin import LinkedInProvider
from providers.unstop import UnstopProvider

class ScraperFactory:
    @staticmethod
    def get_scraper(url: str):
        if "linkedin.com" in url:
            return LinkedInProvider()
        elif "unstop.com" in url:
            return UnstopProvider()
        else:
            raise ValueError("Unsupported platform")