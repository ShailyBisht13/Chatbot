import sys
sys.stdout.reconfigure(encoding='utf-8')
from router import ai_router

# Tourism test
print(ai_router("Best tourism places in Rajasthan for winter."))

# Spiritual test
print(ai_router("Explain meaning of shloka from Bhagavad Gita."))

# Yoga test (NO IMAGE)
print(ai_router("Am I doing yoga correctly?"))

# Monument test (NO IMAGE)
print(ai_router("Identify this monument"))

# General query
print(ai_router("Hello, how are you?"))
