import sys
import os
# Add ai_engine to sys.path
sys.path.append(os.path.join(os.getcwd(), "ai_engine"))

try:
    from meditation_engine import generate_meditation_audio
    print("✅ Successfully imported generate_meditation_audio")
except Exception as e:
    print("❌ Failed to import meditation_engine")
    import traceback
    traceback.print_exc()
