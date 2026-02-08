from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.handlers.chat_handler import ChatHandler

chat_router = APIRouter()

class ChatRequest(BaseModel):
    session_id: str
    message: str
    resume_text: str = ""

@chat_router.post("/chat")
def chat_endpoint(req: ChatRequest):
    try:
        response = ChatHandler.process_chat(req.session_id, req.message, req.resume_text)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))