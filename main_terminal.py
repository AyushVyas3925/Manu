# main_terminal.py – Docker-Enabled Terminal Assistant

import speech_recognition as sr
from response_speaker import speak, say_ready, say_processing
from speech_handler import handle_command
import datetime
import os
import platform
import winsound

from tasks.linux_commands import run_linux_command  ### <-- Added


LOG_FILE = "command_log.txt"

WINDOWS_COMMANDS = [
    "send whatsapp message",
    "send email",
    "get ram info",
    "send sms",
    "make call",
    "google search",
    "play on youtube",
    "take screenshot",
    "get weather",
    "open notepad / calculator / chrome"
]

LINUX_COMMANDS = [
    "list files", "current directory", "disk usage", "memory usage",
    "list processes", "network status", "cpu info", "uptime", "whoami",
    "list users", "kernel version", "os info", "ip address", "list usb devices",
    "list pci devices", "mounted filesystems", "list block devices", "check ports",
    "firewall status", "active services", "failed services", "check cron jobs",
    "check hostname", "view dmesg", "log last reboot", "top processes",
    "recent logins", "disk partitions", "list hidden files", "file permissions",
    "active connections", "available shells", "check bash version", "system date",
    "calendar", "find all users", "group list", "env variables", "list aliases"
]

DOCKER_COMMANDS = [  ### <-- Added
    "list running containers",
    "list all containers",
    "start container",
    "stop container",
    "remove container",
    "list images",
    "remove image",
    "build image",
    "pull image",
    "docker version",
    "docker info",
    "docker networks",
    "docker volumes",
    "docker stats",
    "docker logs",
    "exec into container"
]

def play_beep():
    try:
        if platform.system() == "Windows":
            winsound.Beep(1000, 200)
        else:
            os.system("play -nq -t alsa synth 0.1 sine 1000")
    except:
        pass

def get_audio_from_mic():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    try:
        with mic as source:
            say_ready()
            play_beep()
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
            play_beep()
        say_processing()
        command = recognizer.recognize_google(audio).lower()
        print(f"🧠 You said: {command}")
        return command
    except:
        print("❌ Mic error or unclear speech.")
        return None

def fallback_text_input():
    return input("⌨️ Type your command here: ").lower()

def log_command(command, result):
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log.write(f"[{now}] CMD: {command} => RESULT: {result}\n")

def show_commands(mode, docker=False):
    print("\n📋 Supported commands:")
    if mode == "windows":
        commands = WINDOWS_COMMANDS
    elif docker:
        commands = DOCKER_COMMANDS
    else:
        commands = LINUX_COMMANDS
    for cmd in commands:
        print(f"   • {cmd}")
    print("\n🎤 Speak clearly after the beep...\n")

def main():
    print("\n===== Voice Assistant (Terminal Mode) =====\n")
    mode = input("👉 Enter mode (windows/linux): ").strip().lower()

    if mode not in ["windows", "linux"]:
        print("❌ Invalid mode. Choose either 'windows' or 'linux'")
        return

    docker_mode = False

    if mode == "linux":
        docker_choice = input("🐳 Run Docker command? (yes/no): ").strip().lower()
        docker_mode = docker_choice in ["yes", "y"]

    show_commands(mode, docker=docker_mode)

    while True:
        command_text = get_audio_from_mic()
        if not command_text:
            print("🛑 Trying text input instead.")
            command_text = fallback_text_input()

        if mode == "linux":
            result = run_linux_command(command_text, docker=docker_mode)
        elif mode == "windows":
            result = handle_command(command_text, mode="windows")  # fallback to your handler
        else:
            result = "Unsupported mode."

        print("✅ Result:", result)
        speak(result)
        log_command(command_text, result)

        again = input("\n🔁 Run another command? (y/n): ").strip().lower()
        if again != "y":
            print("👋 Exiting voice assistant.")
            break
        else:
            if mode == "linux":
                docker_choice = input("🐳 Run Docker command again? (yes/no): ").strip().lower()
                docker_mode = docker_choice in ["yes", "y"]
            show_commands(mode, docker=docker_mode)

if __name__ == "__main__":
    main()
