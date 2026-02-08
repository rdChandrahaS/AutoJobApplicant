from typing_extensions import TypedDict, Annotated
from langchain.messages import AnyMessage

class JobState(TypedDict):
    resume_id: str
    user_data: dict
    platform: str
    credentials: dict
    current_job_url: str

