# languages.py — Language mapping and helper functions

LANG_MAP = {
    "en": {"name": "English", "tts": "en"},
    "hi": {"name": "Hindi", "tts": "hi"},
    "bn": {"name": "Bengali", "tts": "bn"},
    "mr": {"name": "Marathi", "tts": "mr"},
    "sa": {"name": "Sanskrit", "tts": "hi"},
}


def lang_name(code: str) -> str:
    """Returns the full language name for a given code (e.g., 'hi' -> 'Hindi')."""
    return LANG_MAP.get(code, LANG_MAP["en"])["name"]
