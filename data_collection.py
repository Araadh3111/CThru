import cv2
import csv
import mediapipe as mp

cam = cv2.VideoCapture(0)

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hand = mp_hands.Hands()

while True:
    rect, frame = cam.read()

    if not rect:
        break

    RGB_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hand.process(RGB_frame)

    row_data = []

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:

            for i in hand_landmarks.landmark:
                row_data.extend([i.x, i.y, i.z])

            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            break  # Record only one hand per frame

    cv2.imshow("Hand Recognition", frame)

    key = cv2.waitKey(1)

    if key == ord('q'):
        break

    elif key == ord('s'):

        if len(row_data) == 63:

            row_data.insert(0, "D")

            with open("hand_data.csv", 'a', newline="") as f:
                writer = csv.writer(f)
                writer.writerow(row_data)

            print("Saved sign D!")

cam.release()
hand.close()
cv2.destroyAllWindows()