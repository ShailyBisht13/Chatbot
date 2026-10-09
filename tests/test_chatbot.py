import sys
sys.stdout.reconfigure(encoding='utf-8')
from router import ai_router

# Tourism
print(ai_router("Best places to visit in Kerala?"))

# Spiritual
print(ai_router("Explain the meaning of Bhagavad Gita shloka 2.47"))

# Yoga (must upload image)
print(ai_router("Am I doing yoga correctly?", "example_pose.jpg"))

# Monument (must upload image)
print(ai_router("Identify this monument", "taj.jpg"))

# General
print(ai_router("Hello"))
