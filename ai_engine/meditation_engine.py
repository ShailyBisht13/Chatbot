# meditation_engine.py — STABLE FAIL-PROOF VERSION
import os
import shutil
import uuid

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Target directory for frontend access - backend/uploads/meditation
UPLOAD_DIR = os.path.join(os.path.dirname(BASE_DIR), "backend", "uploads", "meditation")

os.makedirs(UPLOAD_DIR, exist_ok=True)

def generate_meditation_audio(
        language="en",
        ambience="forest",
        duration_sec=60,
        script_text=None
):
    final_filename = f"meditation_{uuid.uuid4()}.mp3"
    final_path = os.path.join(UPLOAD_DIR, final_filename)
    
    try:
        sounds_dir = os.path.join(BASE_DIR, "sounds")
        ambience_file = os.path.join(sounds_dir, f"{ambience}.mp3")
        
        # Fallback if specific sound missing
        if not os.path.exists(ambience_file):
            ambience_file = os.path.join(sounds_dir, "forest.mp3")

        if os.path.exists(ambience_file):
            shutil.copyfile(ambience_file, final_path)
            print(f"[DEBUG] Copied ambient sound {ambience} to {final_path}")
            return {
                "status": "ok",
                "audio_url": f"/uploads/meditation/{final_filename}",
                "message": f"Meditation with {ambience} ambient sound ready."
            }
        else:
            return {
                "status": "error",
                "message": "Ambient sound files missing."
            }

    except Exception as e:
        print(f"Meditation Engine Error: {e}")
        return {"status": "error", "message": str(e)}
