# voice_output.py — server-side TTS (gTTS) with sentence-safe truncation and cleanup
import os
import re
import time
import uuid
import logging
from gtts import gTTS

logger = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TTS_DIR = os.path.join(os.path.dirname(BASE_DIR), "backend", "uploads", "tts")
os.makedirs(TTS_DIR, exist_ok=True)

SUPPORTED_GTTS_LANGS = {"en", "hi", "bn", "mr"}
MAX_CHARS = 500
FILE_MAX_AGE_SEC = 24 * 3600

_EMOJI = re.compile("[\U0001F000-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF\uFE0F\u200D•●▪]+")
_last_cleanup = 0.0


def sanitize_for_tts(text):
    text = str(text)
    text = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text)      # keep link text, drop URL
    text = _EMOJI.sub(" ", text)
    text = re.sub(r"[#*|`_~>]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= MAX_CHARS:
        return text
    cut = text[:MAX_CHARS]
    # cut at the last sentence end (., !, ?, danda) so the voice doesn't stop mid-sentence
    end = max(cut.rfind(c) for c in (".", "!", "?", "।"))
    return cut[:end + 1] if end > MAX_CHARS * 0.4 else cut


def cleanup_old_files(max_age_sec=FILE_MAX_AGE_SEC):
    """Delete TTS files older than max_age_sec (runs at most once per hour)."""
    global _last_cleanup
    now = time.time()
    if now - _last_cleanup < 3600:
        return
    _last_cleanup = now
    for name in os.listdir(TTS_DIR):
        path = os.path.join(TTS_DIR, name)
        try:
            if os.path.isfile(path) and now - os.path.getmtime(path) > max_age_sec:
                os.remove(path)
        except OSError:
            pass


def generate_tts_audio(text, lang="en"):
    """Returns a relative URL, or None on any failure (never raises)."""
    try:
        cleanup_old_files()
        clean = sanitize_for_tts(text)
        if not clean:
            return None
        filename = f"tts_{uuid.uuid4()}.mp3"
        gTTS(text=clean, lang=lang if lang in SUPPORTED_GTTS_LANGS else "en").save(
            os.path.join(TTS_DIR, filename))
        return f"/uploads/tts/{filename}"
    except Exception as e:
        logger.warning("TTS skipped: %s", e)
        return None