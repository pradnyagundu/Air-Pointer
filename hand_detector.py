import cv2
import mediapipe as mp
import math

class HandDetector:
    def __init__(self, mode=False, maxHands=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon,
        )
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        allHands = []

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                myHand = {}
                lmList = []
                for id, lm in enumerate(handLms.landmark):
                    h, w, _ = img.shape
                    px, py = int(lm.x * w), int(lm.y * h)
                    lmList.append([px, py])
                myHand["lmList"] = lmList
                allHands.append(myHand)

                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

        return allHands, img

    def fingersUp(self, hand):
        lmList = hand["lmList"]
        fingers = []

        # Thumb
        if lmList[4][0] < lmList[3][0]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Fingers: Index to Pinky
        for id in [8, 12, 16, 20]:
            if lmList[id][1] < lmList[id - 2][1]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers
