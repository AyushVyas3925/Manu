# Perform Google search

# tasks/google_search.py – enhanced with optional voice input

import pywhatkit
import speech_recognition as sr
from response_speaker import speak

def listen(prompt="Kya search karna hai?"):
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
        print(f"⚠️ Could not recognize speech: {e}")
        speak("Sorry, mujhe samajh nahi aaya.")
        return None

def google_search(query=None):
    try:
        if not query:
            query = listen("Kya Google par search karna hai?")
            if not query:
                return "❌ No input received for search."

        # Remove 'search' if it's in the start of command
        if query.lower().startswith("search"):
            query = query[len("search"):].strip()

        speak(f"Google par ye search kiya jaa raha hai: {query}")
        pywhatkit.search(query)
        return f"🔎 Googled: {query}"
    except Exception as e:
        return f"❌ Failed to search: {e}"
