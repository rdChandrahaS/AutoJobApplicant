from pydantic import BaseModel, EmailStr
from typing import Optional

class LoginCredentials(BaseModel):
    """
    Schema for logging into platforms.
    """
    platform: str
    username: str
    password: str

class UserProfile(BaseModel):
    """
    Schema for the user's personal details (for auto-filling forms).
    """
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    
    # Context from Resume
    resume_summary: Optional[str] = None
    top_skills: Optional[list[str]] = None