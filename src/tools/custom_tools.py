from datetime import datetime
from langchain_core.tools import tool
import random
import time

@tool
def get_current_time():
    """Returns the current local time."""
    return datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")

def human_like_delay(min_seconds=3, max_seconds=7):
    """
    Sleeps for a random amount of time to mimic human behavior.
    Use this before clicking buttons in Selenium.
    """
    sleep_time = random.uniform(min_seconds, max_seconds)
    print(f"⏳ Acting human... waiting {sleep_time:.2f}s")
    time.sleep(sleep_time)