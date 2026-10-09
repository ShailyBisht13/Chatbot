# llm_engine.py — Unified LLM Engine supporting Google Gemini & Groq with automatic fallback
import os
import base64
import mimetypes
import logging
import requests
import json
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load environment variables across possible candidate locations
for env_path in [
    os.path.join(BASE_DIR, "..", "config", "keys.env"),
    os.path.join(BASE_DIR, "..", ".env"),
    os.path.join(BASE_DIR, "config", "keys.env"),
    os.path.join(BASE_DIR, ".env"),
    "config/keys.env",
    ".env",
]:
    if os.path.exists(env_path):
        load_dotenv(env_path)

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GROQ_CANDIDATE_MODELS = [
    m.strip()
    for m in os.getenv(
        "GROQ_MODELS",
        "openai/gpt-oss-20b,openai/gpt-oss-120b,qwen/qwen3.8-27b,allam-2-7b",
    ).split(",")
    if m.strip()
]
GROQ_VISION_MODEL = os.getenv("GROQ_VISION_MODEL", "llama-3.2-11b-vision-preview")

GEMINI_MODELS = [
    m.strip()
    for m in os.getenv(
        "GEMINI_MODELS",
        "gemini-flash-latest,gemini-flash-lite-latest,gemini-2.5-flash,gemini-1.5-flash",
    ).split(",")
    if m.strip()
]

DEFAULT_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.3"))
MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "2000"))
ERROR_PREFIX = "⚠️ "

# Initialize Groq client if key exists
groq_client = None
if GROQ_API_KEY:
    try:
        from groq import Groq
        groq_client = Groq(api_key=GROQ_API_KEY, timeout=30.0, max_retries=1)
    except Exception as e:
        logger.warning("Failed to initialize Groq client: %s", e)


def is_llm_error(text) -> bool:
    """True if text is one of our error messages."""
    return isinstance(text, str) and text.startswith(ERROR_PREFIX)


# ---------------------------------------------------------
# GOOGLE GEMINI CALLS (Direct REST API for maximum reliability)
# ---------------------------------------------------------
def run_gemini(system_prompt, user_text, temperature=None, max_tokens=None):
    """
    Executes a query against Google Gemini Generative Language API.
    Returns response text or None if failed.
    """
    api_key = os.getenv("GEMINI_API_KEY") or GEMINI_API_KEY
    if not api_key:
        return None

    temp = DEFAULT_TEMPERATURE if temperature is None else temperature
    tokens = max_tokens or MAX_TOKENS

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": f"System Instructions:\n{system_prompt}\n\nUser Request:\n{user_text}"}
                ],
            }
        ],
        "generationConfig": {
            "temperature": temp,
            "maxOutputTokens": tokens,
        },
    }

    for model_name in GEMINI_MODELS:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
        try:
            res = requests.post(
                url,
                headers={"Content-Type": "application/json"},
                json=payload,
                timeout=30,
            )
            if res.status_code == 200:
                data = res.json()
                candidates = data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts and "text" in parts[0]:
                        return parts[0]["text"].strip()
            else:
                logger.warning("Gemini %s returned status %d: %s", model_name, res.status_code, res.text[:200])
        except Exception as e:
            logger.warning("Gemini model %s failed: %s", model_name, e)

    return None


def run_gemini_vision(prompt, image_path):
    """Send image + prompt to Gemini Vision."""
    api_key = os.getenv("GEMINI_API_KEY") or GEMINI_API_KEY
    if not api_key or not image_path or not os.path.isfile(image_path):
        return None

    try:
        mime = mimetypes.guess_type(image_path)[0] or "image/jpeg"
        with open(image_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")

        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt},
                        {
                            "inline_data": {
                                "mime_type": mime,
                                "data": b64,
                            }
                        },
                    ]
                }
            ],
            "generationConfig": {
                "temperature": DEFAULT_TEMPERATURE,
                "maxOutputTokens": 1000,
            },
        }

        for model_name in ["gemini-flash-latest", "gemini-flash-lite-latest", "gemini-2.5-flash"]:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
            res = requests.post(
                url,
                headers={"Content-Type": "application/json"},
                json=payload,
                timeout=35,
            )
            if res.status_code == 200:
                data = res.json()
                candidates = data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts and "text" in parts[0]:
                        return parts[0]["text"].strip()
    except Exception as e:
        logger.warning("Gemini Vision failed: %s", e)

    return None


# ---------------------------------------------------------
# GROQ CALLS
# ---------------------------------------------------------
def run_groq(system_prompt, user_text, temperature=None, max_tokens=None):
    if not groq_client:
        return None

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_text},
    ]
    for model_name in GROQ_CANDIDATE_MODELS:
        try:
            response = groq_client.chat.completions.create(
                model=model_name,
                messages=messages,
                temperature=DEFAULT_TEMPERATURE if temperature is None else temperature,
                max_tokens=max_tokens or MAX_TOKENS,
            )
            content = response.choices[0].message.content
            if content and content.strip():
                return content.strip()
        except Exception as e:
            logger.warning("Groq model %s failed: %s. Trying fallback...", model_name, e)
    return None


# ---------------------------------------------------------
# UNIFIED RUN_LLM (Tries primary -> fallback to alternate provider)
# ---------------------------------------------------------
def run_llm(system_prompt, user_text, temperature=None, max_tokens=None, prefer="auto"):
    """
    Main entry point for LLM generation.
    Supports prefer='gemini', prefer='groq', or 'auto' (checks available keys).
    If one provider fails, automatically falls back to the other!
    """
    gemini_key = os.getenv("GEMINI_API_KEY") or GEMINI_API_KEY
    groq_key = os.getenv("GROQ_API_KEY") or GROQ_API_KEY

    # Priority order
    if prefer == "gemini" and gemini_key:
        ans = run_gemini(system_prompt, user_text, temperature, max_tokens)
        if ans:
            return ans
        if groq_key:
            ans = run_groq(system_prompt, user_text, temperature, max_tokens)
            if ans:
                return ans
    elif prefer == "groq" and groq_key:
        ans = run_groq(system_prompt, user_text, temperature, max_tokens)
        if ans:
            return ans
        if gemini_key:
            ans = run_gemini(system_prompt, user_text, temperature, max_tokens)
            if ans:
                return ans
    else:
        # Default Auto: Prioritize Gemini if key available, otherwise Groq
        if gemini_key:
            ans = run_gemini(system_prompt, user_text, temperature, max_tokens)
            if ans:
                return ans
        if groq_key:
            ans = run_groq(system_prompt, user_text, temperature, max_tokens)
            if ans:
                return ans

    if not groq_key and not gemini_key:
        return ERROR_PREFIX + "AI service unavailable: GROQ_API_KEY or GEMINI_API_KEY missing in environment."

    return ERROR_PREFIX + "Could not generate a response right now. Please try again."


# ---------------------------------------------------------
# UNIFIED VISION LLM
# ---------------------------------------------------------
def run_vision_llm(prompt, image_path):
    """Send an image + prompt to Gemini or Groq vision model."""
    if not image_path or not os.path.isfile(image_path):
        return None

    # Try Gemini vision first if key is available
    if os.getenv("GEMINI_API_KEY") or GEMINI_API_KEY:
        ans = run_gemini_vision(prompt, image_path)
        if ans:
            return ans

    # Fallback to Groq vision
    if groq_client:
        try:
            mime = mimetypes.guess_type(image_path)[0] or "image/jpeg"
            with open(image_path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("utf-8")
            response = groq_client.chat.completions.create(
                model=GROQ_VISION_MODEL,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}},
                        ],
                    }
                ],
                temperature=DEFAULT_TEMPERATURE,
                max_tokens=1000,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.warning("Groq Vision model failed: %s", e)

    return None