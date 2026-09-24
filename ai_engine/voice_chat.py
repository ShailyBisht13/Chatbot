# voice_chat.py
from voice_input import listen
from voice_output import speak
from router import ai_router

def start_voice_chat():
    while True:
        print("\n🎤 Say something or 'stop' to exit")
        query = listen()

        if "stop" in query.lower():
            speak("Stopping voice chat. Goodbye!")
            break

        response = ai_router(query)
        print("Bot:", response)
        speak(response)
