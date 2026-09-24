# voice_output.py — STABLE SERVER-SIDE TTS GENERATION
import os
import re
import uuid
from gtts import gTTS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Save to backend/uploads/tts
TTS_DIR = os.path.join(os.path.dirname(BASE_DIR), "backend", "uploads", "tts")
os.makedirs(TTS_DIR, exist_ok=True)

SUPPORTED_GTTS_LANGS = {"en", "hi", "bn", "mr"}

def sanitize_for_tts(text):
    if not isinstance(text, str):
        text = str(text)
    # Remove markdown headers, tables, bullet symbols, bold/italics
    cleaned = re.sub(r"[#*|`_~]", "", text)
    cleaned = re.sub(r"\[.*?\]\(.*?\)", "", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned[:300]  # Limit length for fast TTS generation

def generate_tts_audio(text, lang="en"):
    """
    Generates a TTS file and returns the relative URL.
    Does NOT crash on errors.
    """
    filename = f"tts_{uuid.uuid4()}.mp3"
    filepath = os.path.join(TTS_DIR, filename)
    
    try:
        clean_text = sanitize_for_tts(text)
        if not clean_text:
            return None

        tts_lang = lang if lang in SUPPORTED_GTTS_LANGS else "en"

        # Generate gTTS
        tts = gTTS(text=clean_text, lang=tts_lang)
        tts.save(filepath)
        
        return f"/uploads/tts/{filename}"

    except Exception as e:
        print(f"[TTS Warning] Generation skipped: {e}")
        return None

def speak(text, lang="en"):
    pass
