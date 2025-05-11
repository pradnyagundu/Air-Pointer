# modules/gesture_actions.py
import pyautogui
import screen_brightness_control as sbc
import os
import datetime

def perform_action(gesture):
    if gesture == "left_click":
        pyautogui.click()
        print("Left Click")
    elif gesture == "right_click":
        pyautogui.click(button='right')
        print("Right Click")
    elif gesture == "volume_up":
        pyautogui.press("volumeup")
        print("Volume Up")
    elif gesture == "volume_down":
        pyautogui.press("volumedown")
        print("Volume Down")
    elif gesture == "screenshot":
        filename = f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        pyautogui.screenshot(filename)
        print(f"Screenshot saved: {filename}")
    elif gesture == "play_pause":
        pyautogui.press("playpause")
        print("Play/Pause Media")
