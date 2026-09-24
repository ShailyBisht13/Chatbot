# voice_engine.py
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import os
import tempfile

# -------------------------------
# Listen from Microphone
# -------------------------------
def listen_user():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Speak now…")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio, language="en-IN")
        print("🗣 You said:", text)
        return text
    except sr.UnknownValueError:
        return "I could not understand. Please repeat."
    except Exception as e:
        return f"Speech error: {str(e)}"


# -------------------------------
# Convert Text → Voice
# -------------------------------
def speak_output(text):
    try:
        tts = gTTS(text=text, lang='en')
        temp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp.name)
        playsound(temp.name)
        os.remove(temp.name)
    except Exception as e:
        print("Voice Output Error:", e)
