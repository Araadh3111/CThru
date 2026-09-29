import cv2
import mediapipe as mp
import pickle 
import numpy as np

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands = 1,
    min_detection_confidence = 0.7
)

cam = cv2.VideoCapture(0)
while True:
    success, frame = cam.read()

    if not success:
        print("Camera not working!")
        break

    
    frame = cv2.flip(frame, 1)

    
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:

            
            row_data = []

            for lm in hand_landmarks.landmark:
                row_data.extend([lm.x, lm.y, lm.z])

            
            wrist_x = row_data[0]
            wrist_y = row_data[1]
            wrist_z = row_data[2]

            for i in range(0, 63, 3):
                row_data[i] -= wrist_x
                row_data[i + 1] -= wrist_y
                row_data[i + 2] -= wrist_z

           
            features = np.array(row_data).reshape(1, 63)

            prediction = model.predict(features)[0]

            
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            
            cv2.putText(
                frame,
                f"Sign: {prediction}",
                (30, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                2,
                (0, 255, 0),
                3
            )

    cv2.imshow("CThru - Sign Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cam.release()
hands.close()
cv2.destroyAllWindows()