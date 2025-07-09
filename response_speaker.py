# response_speaker.py – Enhanced TTS with helper voice cues

import pyttsx3

# 🔧 Initialize TTS engine once
engine = pyttsx3.init()
engine.setProperty('rate', 160)
engine.setProperty('volume', 1.0)

# 🎙 Select English voice
voices = engine.getProperty('voices')
for voice in voices:
    if "english" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

def speak(text):
    try:
        if not text or text.strip().lower() == "none":
            print("⚠️ Nothing to speak.")
            return
        print(f"🗣 Speaking: {text}")
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"🔴 Error speaking text: '{text}' – {e}")

# 🔊 Helper functions for UX cues:
def say_ready():
    speak("Ready. Speak your command now.")

def say_processing():
    speak("Processing your request.")
