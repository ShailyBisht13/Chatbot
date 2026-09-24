# tourism_rag.py
import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from llm_engine import run_llm
from retriever import retrieve

model = SentenceTransformer("all-MiniLM-L6-v2")
BASE_DIR = os.path.dirname(__file__)

# Load tourism prompt
prompt_path = os.path.join(BASE_DIR, "prompts", "tourism_prompt.txt")
with open(prompt_path, "r", encoding="utf-8") as f:
    TOURISM_PROMPT = f.read()

def _search(query, topk=5):
    qv = model.encode([query])[0]
    try:
        return retrieve("tourism_embeds.pt", qv, k=topk)
    except Exception as e:
        print(f"Retrieval error: {e}")
        return []

def answer_tourism_rag(query, lang="en"):
    hits = _search(query, topk=5)
    
    # Filter out empty or dot-only strings
    valid_hits = [h for h in hits if h[0].strip() and h[0].strip() != "."]
    
    if not valid_hits:
        context = "No specific tourism data found in index."
    else:
        # hits is a list of (text, score)
        context = "\n\n".join([f"- {h[0]}" for h in valid_hits])
    
    system = (
        TOURISM_PROMPT
        + f"\n\nSTRICT GEOGRAPHICAL & FACTUAL RULES:\n"
        + f"1. Answer ONLY in {lang}.\n"
        + f"2. Ensure ALL place facts (State, City/District, Region, Nearest Airport, Railway) are 100% accurate.\n"
        + f"3. Do NOT label beaches, waterfalls, or mangrove forests as mountain trekking routes unless they are actual treks.\n"
        + f"4. Provide realistic itineraries (1-day, 3-day, 5-day), transport tips, homestay recommendations, and eco-tips.\n"
        + f"\nContext from Travel Dataset:\n"
        + context
    )
    return run_llm(system, query)

