from llm_engine import run_llm

with open("prompts/tourism_prompt.txt") as f:
    TOURISM_PROMPT = f.read()

def answer_tourism(query):
    return run_llm(TOURISM_PROMPT, query)
