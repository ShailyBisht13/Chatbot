import os
import sys

# Make ai_engine importable no matter where this script is run from
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "ai_engine"))

from meditation_engine import generate_meditation_audio


def test_meditation():
    print("Testing meditation audio generation...")
    result = generate_meditation_audio(ambience="forest", duration_sec=5)
    print(f"Result: {result}")

    if result["status"] != "ok":
        print(f"FAILURE: Engine returned error: {result['message']}")
        return

    audio_path = os.path.join(ROOT, "backend", result["audio_url"].lstrip("/"))
    if os.path.exists(audio_path):
        print(f"SUCCESS: Audio file at {audio_path}")
        print(f"File size: {os.path.getsize(audio_path)} bytes")
        if not result.get("duration_applied"):
            print("NOTE: pydub/ffmpeg unavailable — original clip copied, duration not applied")
    else:
        print(f"FAILURE: Audio file not found at {audio_path}")


if __name__ == "__main__":
    test_meditation()
