# Take a screenshot

# tasks/screenshot.py

import pyautogui
import time
import os

def take_screenshot(save_path="screenshot.png"):
    try:
        time.sleep(2)  # Small delay to allow user to prepare screen
        screenshot = pyautogui.screenshot()
        screenshot.save(save_path)

        abs_path = os.path.abspath(save_path)
        return f"Screenshot saved at {abs_path}"
    except Exception as e:
        return f"Failed to take screenshot: {e}"
