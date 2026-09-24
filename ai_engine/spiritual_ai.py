from llm_engine import run_llm
import json

with open("prompts/spiritual_prompt.txt") as f:
    SPIRITUAL_PROMPT = f.read()

with open("datasets/spiritual/temples.json") as f:
    TEMPLES = json.load(f)

def temple_info(name):
    return TEMPLES.get(name.title(), {})

def answer_spiritual(query):
    return run_llm(SPIRITUAL_PROMPT, query)
