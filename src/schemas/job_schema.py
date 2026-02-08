from pydantic import BaseModel
from typing import Optional, List

class JobSearchQuery(BaseModel):
    """
    Input schema for searching jobs.
    """
    query: str               
    platform: str = "unstop" 
    location: Optional[str] = None

class Job(BaseModel):
    """
    Output schema representing a single job posting.
    """
    title: str
    company: str
    platform: str
    location: Optional[str] = "Unknown"
    job_url: Optional[str] = None
    description: Optional[str] = None
    posted_date: Optional[str] = None
    
    class Config:
        from_attributes = True