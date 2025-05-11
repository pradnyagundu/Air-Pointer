import math

def distance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

def get_gesture(landmarks):
    index_tip = landmarks[8]
    thumb_tip = landmarks[4]
    middle_tip = landmarks[12]
    ring_tip = landmarks[16]
    pinky_tip = landmarks[20]
    palm = landmarks[0]

    dist_thumb_index = distance(thumb_tip, index_tip)
    dist_thumb_middle = distance(thumb_tip, middle_tip)

    # Existing gestures
    if dist_thumb_index < 30:
        return "left_click"
    elif dist_thumb_middle < 30:
        return "right_click"
    elif index_tip[1] < palm[1] and middle_tip[1] < palm[1]:
        return "move_cursor"

    # Screenshot gesture (C-shape): ring and pinky up
    elif ring_tip[1] < palm[1] and pinky_tip[1] < palm[1]:
        return "screenshot"

    # Volume Up
    elif thumb_tip[0] < index_tip[0] and abs(thumb_tip[1] - index_tip[1]) < 30:
        return "volume_up"

    # Volume Down
    elif thumb_tip[0] > index_tip[0] and abs(thumb_tip[1] - index_tip[1]) < 30:
        return "volume_down"

    # Play/Pause (all fingers up - open palm)
    elif all(landmarks[i][1] < landmarks[i - 2][1] for i in [8, 12, 16, 20]):
        return "play_pause"

    else:
        return None
