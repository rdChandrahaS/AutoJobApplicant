from fastapi import FastAPI
from src.routes.chat_router import chat_router
import uvicorn

app = FastAPI(title="AutoJob Backend")
app.include_router(chat_router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)