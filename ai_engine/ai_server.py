from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import uvicorn
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)
for p in [BASE_DIR, PARENT_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from router import ai_router
except ImportError:
    from ai_engine.router import ai_router

app = FastAPI()

class Query(BaseModel):
    query: str
    persona: str = "guide"
    language: str = "en"
    image_path: Optional[str] = None

import traceback

@app.post("/ai")
def ai_chat(data: Query):
    print(f"📥 Received Request: {data.query} (Persona: {data.persona}, Lang: {data.language})")
    try:
        # Call the actual AI engine
        response = ai_router(
            user_input=data.query,
            lang=data.language,
            persona=data.persona,
            image_path=data.image_path
        )
        print(f"📤 Sending Response Status: {response.get('status')}")
        return response
    except Exception as e:
        print("🔥 AI SERVER CRASHED!")
        traceback.print_exc()
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
