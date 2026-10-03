import cv2
import csv
import mediapipe as mp

cam = cv2.VideoCapture(0)
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hand = mp_hands.Hands()

while True:
    rect,frame = cam.read()
    if not rect:
        break
    RGB_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    result = hand.process(RGB_frame)

    row_data = []

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            for i in hand_landmarks.landmark:
                row_data.extend([i.x,i.y,i.z])

            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )
            break

    cv2.imshow("D data colection", frame)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

    elif key == ord('s'):
        if len(row_data)==63:
            wrist_x= row_data[0]
            wrist_y = row_data[1]
            wrist_z = row_data[2]

            for i in range(0,63,3):
                row_data[i]-=wrist_x
                row_data[i+1]-=wrist_y
                row_data[i+2]-= wrist_z

            hand_size = 0

            for i in range(0,63,3):
                distance=(
                    row_data[i]**2+
                    row_data[i+1]**2+
                    row_data[i+2]**2
                ) **0.5

                if distance>hand_size:
                    hand_size = distance         

            if hand_size>0:
                for i in range(63):
                    row_data[i]/=hand_size

            row_data.insert(0,"D")

            with open("webcam_data.csv","a",newline="") as f:
                writer = csv.writer(f)
                writer.writerow(row_data)

            print('Saved Sign D')
cam.release()
hand.close()
cv2.destroyAllWindows()