import os
import sys
from fastapi import FastAPI
from pydantic import BaseModel

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from router import ai_router

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    language: str = "en"
    user_id: str | None = None

@app.post("/chat")
def chat(req: ChatRequest):
    result = ai_router(
        user_input=req.message,
        lang=req.language
    )
    return {
        "reply": result.get("answer", "") if isinstance(result, dict) else str(result),
        "data": result
    }
