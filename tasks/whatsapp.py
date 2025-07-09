# tasks/whatsapp.py – improved WhatsApp sender with voice/manual input

import pywhatkit
import time
import speech_recognition as sr
from response_speaker import speak

def listen(prompt="Bol kar bataye"):
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
        speak("Mujhe samajh nahi aaya. Aap manually type kar sakte hain.")
        return input(f"📝 {prompt} (type here): ")

def send_whatsapp_message(phone_number=None, message=None):
    try:
        # Take phone number via voice or manual
        if not phone_number:
            phone_input = listen("Kisko WhatsApp message bhejna hai? Phone number bataye with country code.")
            phone_input = phone_input.replace(" ", "").replace("-", "")
            if not phone_input.startswith("+"):
                phone_input = "+91" + phone_input
            phone_number = phone_input

        # Take message via voice or manual
        if not message:
            message = listen("Kya message bhejna hai? Bataye.")
        
        # Validate
        if not phone_number or not message:
            return "❌ Phone number ya message nahi mila."

        print(f"📤 Sending WhatsApp message to {phone_number}: {message}")
        pywhatkit.sendwhatmsg_instantly(phone_number, message, wait_time=10, tab_close=True)
        speak(f"Message bhej diya gaya {phone_number} par.")
        return f"✅ Message sent to {phone_number}: {message}"

    except Exception as e:
        print(f"❌ Error: {e}")
        speak("Message bhejne me error aaya.")
        return f"❌ Failed to send message: {e}"
