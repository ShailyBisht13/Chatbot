# meditation_engine.py — ambient audio, trimmed/looped to the requested duration
import os
import shutil
import logging

logger = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOUNDS_DIR = os.path.join(BASE_DIR, "sounds")
UPLOAD_DIR = os.path.join(os.path.dirname(BASE_DIR), "backend", "uploads", "meditation")
os.makedirs(UPLOAD_DIR, exist_ok=True)

VALID_AMBIENCE = {"forest", "river", "wind", "rain"}


def _build_clip(src, dst, duration_sec):
    """Loop/trim with pydub (needs ffmpeg). Returns True if duration was applied."""
    try:
        from pydub import AudioSegment
        audio = AudioSegment.from_file(src)
        target_ms = int(duration_sec * 1000)
        looped = audio * (target_ms // max(len(audio), 1) + 1)
        looped[:target_ms].fade_in(2000).fade_out(3000).export(dst, format="mp3")
        return True
    except Exception as e:
        logger.warning("pydub unavailable/failed (%s); copying original file", e)
        shutil.copyfile(src, dst)
        return False


def generate_meditation_audio(ambience="forest", duration_sec=60):
    """
    Deterministic file name (ambience + duration) => files are created once and reused,
    so the uploads folder no longer grows by one file per request.
    Removed the unused `language` / `script_text` parameters.
    """
    ambience = ambience if ambience in VALID_AMBIENCE else "forest"
    src = os.path.join(SOUNDS_DIR, f"{ambience}.mp3")
    if not os.path.exists(src):
        ambience, src = "forest", os.path.join(SOUNDS_DIR, "forest.mp3")
    if not os.path.exists(src):
        return {"status": "error", "message": "Ambient sound files missing."}

    filename = f"meditation_{ambience}_{int(duration_sec)}s.mp3"
    dst = os.path.join(UPLOAD_DIR, filename)
    try:
        applied = True
        if not os.path.exists(dst):
            applied = _build_clip(src, dst, duration_sec)
        return {
            "status": "ok",
            "audio_url": f"/uploads/meditation/{filename}",
            "ambience": ambience,
            "duration_applied": applied,
            "message": f"Meditation with {ambience} ambient sound ready.",
        }
    except Exception as e:
        logger.error("Meditation engine error: %s", e)
        return {"status": "error", "message": str(e)}