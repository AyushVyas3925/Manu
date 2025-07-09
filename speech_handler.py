from tasks.whatsapp import send_whatsapp_message
from tasks.email import send_email
from tasks.ram_info import get_ram_info
from tasks.sms import send_sms
from tasks.call import make_call
from tasks.google_search import google_search
from tasks.youtube_play import play_on_youtube
from tasks.screenshot import take_screenshot
from tasks.weather import get_weather
from tasks.open_apps import open_app
from tasks.linux_commands import run_linux_command
from response_speaker import speak
import speech_recognition as sr

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
        speak("Samajh nahi aaya. Type karke bataye.")
        return input(f"📝 {prompt} (type here): ")

def handle_command(command, mode="windows", docker=False):  # <-- docker flag added
    try:
        command = command.lower()

        if mode == "linux":
            return run_linux_command(command, docker=docker)  # <-- docker mode passed

        # Windows-specific tasks:
        if "whatsapp" in command:
            return send_whatsapp_message()

        elif "email" in command:
            sender_email = "your_email@gmail.com"
            sender_password = "your_email_password"  # Replace with your email App password

            receiver_email = listen("Receiver ka email bataye.")
            subject = listen("Subject kya hai?")
            body = listen("Message body kya likhna hai?")

            return send_email(sender_email, sender_password, receiver_email, subject, body)

        elif "ram" in command or "memory" in command:
            return get_ram_info()

        elif "sms" in command:
            return send_sms("twilio_sid", "twilio_auth_token", "twilio_phone_number",
                            "verified_twilio_number", "Test SMS from assistant")

        elif "call" in command:
            return make_call("twilio_sid", "twilio_auth_token", "twilio_phone_number",
                             "verified_twilio_number", "https://handler.twilio.com/twiml/YOUR_ID")

        elif "search" in command or "google" in command:
            return google_search(command)

        elif "youtube" in command or "play" in command:
            return play_on_youtube(command)

        elif "screenshot" in command:
            return take_screenshot()

        elif "weather" in command:
            return get_weather("jaipur", "86f5ce08370555e54a1293ce40749573")

        elif "calculator" in command:
            return open_app("calculator")
        
        elif "notepad" in command:
            return open_app("notepad")
        
        elif "chrome" in command:
            return open_app("chrome")

        return "Sorry, I didn't understand the command."

    except Exception as e:
        return f"Command error: {e}"
