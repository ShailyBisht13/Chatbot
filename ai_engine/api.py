from fastapi import FastAPI
from pydantic import BaseModel
from main_chatbot import get_chat_response  # adapt name if different

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    language: str = "en"
    user_id: str | None = None

@app.post("/chat")
def chat(req: ChatRequest):
    reply = get_chat_response(
        query=req.message,
        language=req.language,
        user_id=req.user_id
    )
    return {
        "reply": reply
    }
