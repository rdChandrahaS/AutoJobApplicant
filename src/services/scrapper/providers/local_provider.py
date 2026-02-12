import time
from selenium.webdriver.common.by import By
from src.services.interfaces.ScraperProvider import ScraperProvider

class LocalScraper(ScraperProvider):
    """
    Scraper for the Local Mock Job Portal running on localhost:8001.
    """
    
    # Matches the mock server port
    BASE_URL = "http://127.0.0.1:8001"

    def login(self, username, password) -> tuple[bool, str]:
        print(f"[LocalScraper] Navigating to {self.BASE_URL}/login...")
        try:
            self.driver.get(f"{self.BASE_URL}/login")
            time.sleep(1) 
            
            self.driver.find_element(By.ID, "email").send_keys(username)
            self.driver.find_element(By.ID, "password").send_keys(password)
            self.driver.find_element(By.ID, "submit-login").click()
            
            time.sleep(1)
            
            if "jobs" in self.driver.current_url:
                return True, "Successfully logged into LocalHost Jobs"
            return False, "Login failed: Redirect didn't happen"
            
        except Exception as e:
            return False, f"Login error: {str(e)}"

    def search_jobs(self, query) -> tuple[bool, list]:
        print(f"[LocalScraper] Searching for '{query}'...")
        try:
            search_url = f"{self.BASE_URL}/jobs?q={query}"
            self.driver.get(search_url)
            time.sleep(1)
            
            job_elements = self.driver.find_elements(By.CLASS_NAME, "job-card")
            jobs_data = []
            
            for el in job_elements:
                try:
                    title_el = el.find_element(By.CLASS_NAME, "job-title").find_element(By.TAG_NAME, "a")
                    company_el = el.find_element(By.CLASS_NAME, "company-name")
                    location_el = el.find_element(By.CLASS_NAME, "job-location")
                    desc_el = el.find_element(By.CLASS_NAME, "job-desc")
                    
                    jobs_data.append({
                        "title": title_el.text,
                        "company": company_el.text,
                        "location": location_el.text.replace("📍 ", ""),
                        "job_url": title_el.get_attribute("href"),
                        "description": desc_el.text,
                        "platform": "local",
                        "posted_date": "Just now"
                    })
                except Exception as inner_e:
                    print(f"Skipping a malformed job card: {inner_e}")
                    continue
            
            return True, jobs_data
            
        except Exception as e:
            return False, f"Search failed: {str(e)}"