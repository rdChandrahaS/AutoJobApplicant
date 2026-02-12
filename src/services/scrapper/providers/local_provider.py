import os
import time
from selenium.webdriver.common.by import By
from src.services.interfaces.ScraperProvider import ScraperProvider

class LocalScraper(ScraperProvider):
    """
    Scraper for the Local Mock Job Portal.
    """
    def __init__(self, driver):
        self.driver = driver
        self.base_url = os.getenv("MOCK_PORTAL_URL", "http://127.0.0.1:8001")

    def login(self, username, password) -> tuple[bool, str]:
        print(f"[LocalScraper] Navigating to {self.base_url}/login...")
        try:
            self.driver.get(f"{self.base_url}/login")
            time.sleep(1) 
            
            try:
                self.driver.find_element(By.ID, "email").send_keys(username)
                self.driver.find_element(By.ID, "password").send_keys(password)
                submit_btn = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
                submit_btn.click()
            except:
                pass
            
            time.sleep(1)
            
            return True, "Successfully logged into LocalHost Jobs"
            
        except Exception as e:
            return False, f"Login error: {str(e)}"

    def search_jobs(self, query) -> tuple[bool, list]:
        print(f"[LocalScraper] Searching for '{query}'...")
        try:
            search_url = f"{self.base_url}/"
            self.driver.get(search_url)
            time.sleep(1)
            
            job_cards = self.driver.find_elements(By.CLASS_NAME, "job-card")
            jobs_data = []
            
            for card in job_cards:
                try:
                    title = card.find_element(By.TAG_NAME, "h5").text
                    
                    company = card.find_element(By.TAG_NAME, "p").text
                    
                    location = "Remote"
                    all_spans = card.find_elements(By.TAG_NAME, "span")
                    for span in all_spans:
                        if "📍" in span.text:
                            location = span.text.replace("📍", "").strip()
                            break

                    link_el = card.find_element(By.CLASS_NAME, "btn-apply")
                    job_url = link_el.get_attribute("href")
                    
                    jobs_data.append({
                        "title": title,
                        "company": company,
                        "location": location,
                        "job_url": job_url,
                        "description": f"Job at {company}", 
                        "platform": "local",
                        "posted_date": "Just now"
                    })
                except Exception as inner_e:
                    print(f"Skipping malformed card: {inner_e}")
                    continue
            
            return True, jobs_data
            
        except Exception as e:
            return False, f"Search failed: {str(e)}"