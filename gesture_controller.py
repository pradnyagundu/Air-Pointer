import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time
import math

# Initialize MediaPipe Hands
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Capture from webcam
cap = cv2.VideoCapture(0)
screen_width, screen_height = pyautogui.size()

# Helper for distance
def get_distance(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

# Start MediaPipe Hands
with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7) as hands:
    prev_time = 0

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue

        # Flip image
        image = cv2.flip(image, 1)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                h, w, _ = image.shape

                # Get landmarks
                landmarks = []
                for lm in hand_landmarks.landmark:
                    lmx, lmy = int(lm.x * w), int(lm.y * h)
                    landmarks.append((lmx, lmy))

                # Cursor control - index finger tip
                index_tip = landmarks[8]
                pyautogui.moveTo(index_tip[0] * screen_width / w, index_tip[1] * screen_height / h)

                # Gesture Detection
                thumb_tip = landmarks[4]
                middle_tip = landmarks[12]

                # Left click: Index + Thumb
                if get_distance(index_tip, thumb_tip) < 40:
                    pyautogui.click()
                    time.sleep(0.3)

                # Right click: Middle + Thumb
                elif get_distance(middle_tip, thumb_tip) < 40:
                    pyautogui.rightClick()
                    time.sleep(0.3)

                # Screenshot gesture (make "C" shape)
                pinky_tip = landmarks[20]
                if get_distance(index_tip, pinky_tip) < 50:
                    pyautogui.screenshot('screenshot.png')
                    print("📸 Screenshot Taken!")
                    time.sleep(0.5)

                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # FPS counter
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time)
        prev_time = curr_time
        cv2.putText(image, f'FPS: {int(fps)}', (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow('Air Pointer Pro', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
