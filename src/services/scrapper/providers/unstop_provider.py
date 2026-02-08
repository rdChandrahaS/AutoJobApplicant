from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from src.services.interfaces.ScraperProvider import ScraperProvider
from src.tools.custom_tools import human_like_delay

class UnstopScraper(ScraperProvider):
    def login(self, username, password):
        try:
            self.driver.get("https://unstop.com/auth/login")
            human_like_delay(3, 5)
            self.driver.find_element(By.ID, "username").send_keys(username)
            human_like_delay(1, 2)
            self.driver.find_element(By.ID, "password").send_keys(password)
            human_like_delay(1, 3)
            self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
            human_like_delay(5, 7)
            return True, f"✅ Logged in to Unstop as {username}"
        except Exception as e:
            return False, f"❌ Unstop Login Failed: {str(e)}"

    def search_jobs(self, query):
        try:
            try: search_box = self.driver.find_element(By.TAG_NAME, "input")
            except: search_box = self.driver.find_element(By.CSS_SELECTOR, "input[type='search']")
            
            search_box.send_keys(query)
            human_like_delay(1, 2)
            search_box.send_keys(Keys.RETURN)
            return True, f"✅ Searched for '{query}'"
        except Exception as e:
            return False, f"⚠️ Search Failed: {str(e)}"