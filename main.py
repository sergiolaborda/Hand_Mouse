import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import keyboard

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
cap = cv2.VideoCapture(0)
x, y = pyautogui.size()
estado_mouse = 0  # 0=arriba, 1 = abajo


def calculate_distance(x1, y1, x2, y2):
    p1 = np.array([x1, y1])
    p2 = np.array([x2, y2])
    return np.linalg.norm(p1 - p2)


def detect_finger_down(hand_landmarks):
    finger_down = False

    x_base1 = int(hand_landmarks.landmark[0].x * 100)
    y_base1 = int(hand_landmarks.landmark[0].y * 100)

    x_base2 = int(hand_landmarks.landmark[9].x * 100)
    y_base2 = int(hand_landmarks.landmark[9].y * 100)

    x_index = int(hand_landmarks.landmark[8].x * 100)
    y_index = int(hand_landmarks.landmark[8].y * 100)

    d_base = calculate_distance(x_base1, y_base1, x_base2, y_base2)
    d_base_index = calculate_distance(x_base1, y_base1, x_index, y_index)

    if d_base_index < d_base:
        finger_down = True
    return finger_down


with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.5) as hands:
    while True:
        ret, frame = cap.read()
        if ret == False:
            break
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(frame_rgb)
        w=0
        if results.multi_hand_landmarks is not None:
            for hand_landmarks in results.multi_hand_landmarks:
                x1 = int(x * hand_landmarks.landmark[9].x)
                y1 = int(y * hand_landmarks.landmark[9].y)
                if results.multi_handedness[w].classification[0].label == "Right":
                    pyautogui.moveTo(x1, y1)
                    if detect_finger_down(hand_landmarks):
                        if estado_mouse == 0:
                            pyautogui.mouseDown()
                            estado_mouse = 1
                    else:
                        if estado_mouse == 1:
                            pyautogui.mouseUp()
                            estado_mouse = 0
                else:
                    if detect_finger_down(hand_landmarks):
                        pyautogui.keyDown("w")
                    else:
                        pyautogui.keyUp("w")

                w=w+1

                # pyautogui.moveTo(int(hand_landmarks.landmark[9].x), int(hand_landmarks.landmark[9].y))
                # cv2.circle(output, (hand_landmarks.landmark[9].x, hand_landmarks.landmark[9].y), 10, color_mouse_pointer, 3)
                # cv2.circle(output, (hand_landmarks.landmark[9].x, hand_landmarks.landmark[9].y), 5, color_mouse_pointer, -1)
                """
                A trabajar el click
                pyautogui.mouseDown(); pyautogui.mouseUp()  # does the same thing as a left-button mouse click
                pyautogui.mouseDown(button='right')  # press the right button down
                pyautogui.mouseUp(button='right', x=100, y=200)  # move the mouse to 100, 200, then release the right button up.
                """

        # cv2.imshow('output', output)

cap.release()
cv2.destroyAllWindows()