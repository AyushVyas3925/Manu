import streamlit as st
from speech_handler import handle_command
from tasks.linux_commands import run_linux_command
import speech_recognition as sr

# Available commands
WINDOWS_COMMANDS = [
    "send whatsapp message", "send email", "get ram info", "send sms", "make call",
    "google search", "play on youtube", "take screenshot", "get weather",
    "open notepad", "open calculator", "open chrome"
]

LINUX_COMMANDS = [
    "list files", "current directory", "disk usage", "memory usage", "list processes",
    "network status", "cpu info", "uptime", "whoami", "list users", "kernel version",
    "os info", "ip address", "list usb devices", "list pci devices", "mounted filesystems",
    "list block devices", "check ports", "firewall status", "active services",
    "failed services", "check cron jobs", "check hostname", "view dmesg", "log last reboot",
    "top processes", "recent logins", "disk partitions", "list hidden files",
    "file permissions", "active connections", "available shells", "check bash version",
    "system date", "calendar", "find all users", "group list", "env variables", "list aliases"
]

DOCKER_COMMANDS = [
    "list running containers", "list all containers", "start container", "stop container",
    "remove container", "list images", "remove image", "build image", "pull image",
    "docker version", "docker info", "docker networks", "docker volumes",
    "docker stats", "docker logs", "exec into container"
]

def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙️ Listening... Speak your command now.")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        st.success(f"🧠 You said: {text}")
        return text
    except:
        st.error("❌ Could not recognize voice.")
        return ""

# Streamlit Setup
st.set_page_config("Voice Assistant", layout="centered")
st.title("🎙️ Voice + Docker Terminal Assistant")
st.markdown("Use Windows / Linux / Docker commands with voice or manual input.")

mode = st.selectbox("🧭 Select Mode:", ["windows", "linux"])
docker_mode = False
if mode == "linux":
    docker_mode = st.toggle("🐳 Enable Docker Commands")

st.markdown("---")

if docker_mode:
    st.subheader("📦 Docker Commands")
    selected_command = st.selectbox("Choose a Docker Command:", DOCKER_COMMANDS)
    if st.button("▶️ Run Docker Command"):
        with st.spinner("Running Docker command..."):
            result = run_linux_command(selected_command, docker=True)
        st.success("✅ Output")
        st.code(result)

else:
    st.subheader("🎤 Voice or Text Command")

    # Voice input
    if st.button("🎙️ Use Voice"):
        spoken = recognize_speech()
        st.session_state["spoken_command"] = spoken
        st.session_state["auto_run_voice"] = True

    if "spoken_command" not in st.session_state:
        st.session_state["spoken_command"] = ""
    if "auto_run_voice" not in st.session_state:
        st.session_state["auto_run_voice"] = False

    command_input = st.text_input("📝 Or type your command manually:", key="typed_command", value=st.session_state["spoken_command"])

    command_to_run = command_input.strip().lower()

    # Interactive Form for Email
    if "email" in command_to_run:
        with st.form("email_form"):
            st.markdown("📧 **Send Email**")
            receiver = st.text_input("Receiver Email")
            subject = st.text_input("Subject")
            body = st.text_area("Message")
            submitted = st.form_submit_button("📨 Send Email")
            if submitted:
                from tasks.email import send_email
                result = send_email("your_email@gmail.com", "your_app_password", receiver, subject, body)
                st.success("✅ Email Result")
                st.code(result)

    # Interactive Form for WhatsApp
    elif "whatsapp" in command_to_run:
        with st.form("whatsapp_form"):
            st.markdown("💬 **Send WhatsApp Message**")
            number = st.text_input("Phone Number (+91...)")
            message = st.text_area("Message")
            submitted = st.form_submit_button("📤 Send WhatsApp")
            if submitted:
                from tasks.whatsapp import send_whatsapp_message
                result = send_whatsapp_message(number, message)
                st.success("✅ WhatsApp Result")
                st.code(result)

    # Auto-run command (from voice)
    elif st.session_state["auto_run_voice"] and command_to_run != "":
        st.session_state["auto_run_voice"] = False
        with st.spinner("Running voice command..."):
            result = handle_command(command_to_run, mode=mode)
        st.success("✅ Output")
        st.code(result)

    # Manual run
    elif st.button("▶️ Run Command"):
        if command_to_run == "":
            st.warning("❗ Please speak or type a command.")
        else:
            with st.spinner("Processing..."):
                result = handle_command(command_to_run, mode=mode)
            st.success("✅ Output")
            st.code(result)

# Show available commands
st.markdown("---")
st.subheader("📋 Available Commands")
commands = DOCKER_COMMANDS if docker_mode else (WINDOWS_COMMANDS if mode == "windows" else LINUX_COMMANDS)
for i, cmd in enumerate(commands, start=1):
    st.markdown(f"`{i}. {cmd}`")
