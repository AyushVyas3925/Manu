# Open desktop apps

# tasks/open_apps.py

import os
import platform
import subprocess

def open_app(app_name):
    try:
        app_name = app_name.lower()

        if platform.system() != "Windows":
            return "This feature is currently supported only on Windows."

        if app_name == "notepad":
            os.system("notepad")
        elif app_name == "calculator":
            os.system("calc")
        elif app_name == "chrome":
            subprocess.Popen("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
        elif app_name == "command prompt" or app_name == "cmd":
            os.system("start cmd")
        else:
            return f"App '{app_name}' not supported yet."

        return f"Opening {app_name}..."
    except Exception as e:
        return f"Failed to open app: {e}"

