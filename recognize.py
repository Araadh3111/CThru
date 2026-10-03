import cv2
import mediapipe as mp
import pickle
import numpy as np


with open("model.pkl", "rb") as f:
    model = pickle.load(f)


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7
)


cam = cv2.VideoCapture(0)

while True:

    success, frame = cam.read()

    if not success:
        print("Camera not working!")
        break

    # Keep original frame for MediaPipe
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = hands.process(rgb)

    prediction = None
    confidence = 0

    if result.multi_hand_landmarks:

        for hand_landmarks in result.multi_hand_landmarks:

           

            row_data = []

            for lm in hand_landmarks.landmark:

                row_data.extend([
                    lm.x,
                    lm.y,
                    lm.z
                ])

        

            wrist_x = row_data[0]
            wrist_y = row_data[1]
            wrist_z = row_data[2]

            for i in range(0, 63, 3):

                row_data[i] -= wrist_x
                row_data[i + 1] -= wrist_y
                row_data[i + 2] -= wrist_z

            

            hand_size = 0

            for i in range(0, 63, 3):

                distance = (
                    row_data[i] ** 2 +
                    row_data[i + 1] ** 2 +
                    row_data[i + 2] ** 2
                ) ** 0.5

                if distance > hand_size:
                    hand_size = distance

            if hand_size > 0:

                for i in range(63):
                    row_data[i] /= hand_size

            

            features = np.array(row_data).reshape(1, 63)

            

            prediction = model.predict(features)[0]

            probabilities = model.predict_proba(features)[0]

            confidence = max(probabilities) * 100

            
            top_3 = probabilities.argsort()[-3:][::-1]

            print("\nTop Predictions:")

            for i in top_3:

                print(
                    model.classes_[i],
                    f"{probabilities[i] * 100:.1f}%"
                )

           

            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

   

    frame = cv2.flip(frame, 1)

   

    if prediction is not None:

        cv2.putText(
            frame,
            f"Sign: {prediction} ({confidence:.1f}%)",
            (30, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.5,
            (0, 255, 0),
            3
        )

    cv2.imshow(
        "CThru - Sign Recognition",
        frame
    )

    
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break



cam.release()
hands.close()
cv2.destroyAllWindows()