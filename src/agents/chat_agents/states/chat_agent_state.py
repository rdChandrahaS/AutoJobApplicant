from typing import TypedDict, Annotated, List, Dict, Optional
from langchain_core.messages import BaseMessage
import operator

class ChatAgentState(TypedDict):
    """
    Defines the memory structure of the agent.
    """
    # Chat History
    messages: Annotated[List[BaseMessage], operator.add]
    
    # Resume Context
    resume_text: str 
    summary: str
    
    # Job Application Context
    platform: str
    job_query: str 
    credentials: Dict[str, str]