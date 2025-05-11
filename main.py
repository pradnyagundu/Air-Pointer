import cv2
import numpy as np
import pyautogui
import time
import math
from modules.hand_detector import HandDetector
from modules.gesture_mapper import get_gesture
from modules.gesture_actions import perform_action
from modules.gui_feedback import show_feedback

# Screen size
screen_width, screen_height = pyautogui.size()

# Initialize camera
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Hand detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

prev_y = None
scroll_threshold = 30
click_cooldown = 0.6  # seconds
last_click_time = 0

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)

    if hands:
        hand = hands[0]
        lmList = hand["lmList"]

        if len(lmList) >= 21:
            # Cursor Movement
            x, y = lmList[8]
            screen_x = np.interp(x, [0, 640], [0, screen_width])
            screen_y = np.interp(y, [0, 480], [0, screen_height])
            pyautogui.moveTo(screen_x, screen_y)

            # Scroll Gesture
            center_y = lmList[0][1]
            if prev_y is not None:
                diff = prev_y - center_y
                if diff > scroll_threshold:
                    pyautogui.scroll(20)
                    show_feedback(img, "Scrolling Up")
                elif diff < -scroll_threshold:
                    pyautogui.scroll(-20)
                    show_feedback(img, "Scrolling Down")
            prev_y = center_y

            # Gesture Recognition and Action
            gesture = get_gesture(lmList)
            if gesture and time.time() - last_click_time > click_cooldown:
                perform_action(gesture)
                show_feedback(img, f"Gesture: {gesture}")
                last_click_time = time.time()

    cv2.imshow("Air Pointer Pro", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
