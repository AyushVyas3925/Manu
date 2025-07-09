# tasks/youtube_play.py – Voice-enabled YouTube player

import pywhatkit
import speech_recognition as sr
from response_speaker import speak

def listen(prompt="Kya YouTube pe play karna hai?"):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    speak(prompt)

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("🎤 Listening...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio).strip()
        print(f"🧠 You said: {text}")
        return text
    except Exception as e:
        print(f"⚠️ Speech error: {e}")
        speak("Sorry, kuch samajh nahi aaya.")
        return None

def play_on_youtube(query=None):
    try:
        if not query:
            query = listen("Kaunsa song ya video play karna hai?")
            if not query:
                return "❌ No input given."

        # Remove unnecessary voice parts
        keywords = ["play", "song", "on youtube", "video"]
        for k in keywords:
            query = query.replace(k, "").strip()

        if not query:
            query = "lofi music"

        speak(f"YouTube par chalu kiya jaa raha hai: {query}")
        pywhatkit.playonyt(query)
        return f"▶️ Playing '{query}' on YouTube"

    except Exception as e:
        return f"❌ Failed to play: {e}"
