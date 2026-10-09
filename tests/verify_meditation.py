import os
import sys

# Add ai_engine to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), "ai_engine"))

from ai_engine.meditation_engine import generate_meditation_audio

def test_meditation():
    print("Testing meditation audio generation...")
    # Test with existing but corrupted file (forest)
    result = generate_meditation_audio(language="en", ambience="forest", duration_sec=5)
    print(f"Result: {result}")
    
    if result["status"] == "ok":
        audio_path = os.path.join("backend", result["audio_url"].lstrip("/"))
        if os.path.exists(audio_path):
            print(f"SUCCESS: Audio file generated at {audio_path}")
            print(f"File size: {os.path.getsize(audio_path)} bytes")
        else:
            print(f"FAILURE: Audio file not found at {audio_path}")
    else:
        print(f"FAILURE: Engine returned error: {result['message']}")

if __name__ == "__main__":
    test_meditation()
