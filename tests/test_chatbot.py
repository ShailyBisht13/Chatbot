import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

# Make ai_engine importable no matter where this script is run from
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "ai_engine"))

from router import ai_router


def img(name):
    """Resolve an image next to this script; warn if it's missing."""
    path = os.path.join(ROOT, name)
    if not os.path.isfile(path):
        print(f"⚠️ {name} not found — running without image")
        return None
    return path


# Tourism
print(ai_router("Best places to visit in Kerala?"))

# Spiritual
print(ai_router("Explain the meaning of Bhagavad Gita shloka 2.47"))

# Yoga (with image)
print(ai_router("Am I doing yoga correctly?", image_path=img("example_pose.jpg")))

# Monument (with image)
print(ai_router("Identify this monument", image_path=img("taj.jpg")))

# General
print(ai_router("Hello"))
