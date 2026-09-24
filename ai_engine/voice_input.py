# voice_input.py
import speech_recognition as sr

def listen():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("🎤 Speak now...")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except Exception as e:
        return "I could not understand your speech."
