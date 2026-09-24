import os
from groq import Groq
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Candidate Groq models in order of priority
CANDIDATE_MODELS = [
    "openai/gpt-oss-20b",
    "qwen/qwen3.8-27b",
    "openai/gpt-oss-120b"
]

# Load environment variables
for env_path in [
    os.path.join(BASE_DIR, "..", "config", "keys.env"),
    os.path.join(BASE_DIR, "..", ".env"),
    os.path.join(BASE_DIR, "config", "keys.env"),
    os.path.join(BASE_DIR, ".env"),
    "config/keys.env",
    ".env"
]:
    if os.path.exists(env_path):
        load_dotenv(env_path)

api_key = os.getenv("GROQ_API_KEY")

client = None
if api_key:
    try:
        client = Groq(api_key=api_key)
    except Exception as e:
        print(f"Warning: Failed to initialize Groq client: {e}")

def run_llm(system_prompt, user_text):
    if not client:
        return "AI response service unavailable (Groq API key missing)."

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_text}
    ]

    last_error = None
    for model_name in CANDIDATE_MODELS:
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=messages,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"[LLM Warning] Model {model_name} failed: {e}. Trying fallback...")
            last_error = e

    return f"Unable to generate response from AI models. (Error: {last_error})"
