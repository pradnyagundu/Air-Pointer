# modules/gui_feedback.py
import cv2

def show_feedback(frame, text):
    cv2.putText(frame, text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 255, 0), 3, cv2.LINE_AA)
