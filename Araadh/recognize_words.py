import cv2
import mediapipe as mp
import pickle
import numpy as np
import pyttsx3

engine = pyttsx3.init()

with open("model_webcam.pkl", "rb") as f:
    model = pickle.load(f)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7
)

cam = cv2.VideoCapture(0)

text = ""

last_prediction = None
prediction_count = 0
required_count = 8

confidence_history = []

locked_prediction = None

no_hand_count = 0
required_no_hand = 5

while True:

    success, frame = cam.read()

    if not success:
        print("camera not working")
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    prediction = None
    confidence = 0

    if result.multi_hand_landmarks:

        no_hand_count = 0

        hand_landmarks = result.multi_hand_landmarks[0]

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

        mp_drawing.draw_landmarks(
            frame,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS
        )

        if prediction == last_prediction:

            prediction_count += 1
            confidence_history.append(confidence)

        else:

            last_prediction = prediction
            prediction_count = 1
            confidence_history = [confidence]

        if prediction_count >= required_count:

            average_confidence = sum(confidence_history) / len(confidence_history)

            if prediction != locked_prediction:

                if prediction == "clear" or prediction == "backspace":
                    required_confidence = 30
                else:
                    required_confidence = 50

                if average_confidence >= required_confidence:

                    if prediction == "space":

                        text += " "

                        print(
                            f"Confirmed: SPACE "
                            f"({average_confidence:.1f}%)"
                        )

                    elif prediction == "clear":

                        text = ""

                        print("Confirmed: CLEAR")

                    elif prediction == "backspace":

                        text = text[:-1]

                        print("Confirmed: BACKSPACE")

                    else:

                        text += prediction

                        print(
                            f"Confirmed: {prediction} "
                            f"({average_confidence:.1f}%)"
                        )

                    locked_prediction = prediction

                prediction_count = 0
                confidence_history = []

    else:

        no_hand_count += 1

        prediction_count = 0
        last_prediction = None
        confidence_history = []

        if no_hand_count >= required_no_hand:

            locked_prediction = None

    frame = cv2.flip(frame, 1)

    if prediction is not None:

        cv2.putText(
            frame,
            f"Sign: {prediction} ({confidence:.1f}%)",
            (30, 55),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.1,
            (0, 255, 0),
            3
        )

    display_text = text

    if len(display_text) > 35:
        display_text = display_text[-35:]

    cv2.putText(
        frame,
        f"Text: {display_text}",
        (30, 105),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"Stable: {prediction_count}/{required_count}",
        (30, 145),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    cv2.imshow(
        "CThru - Word Recognition",
        frame
    )

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

cam.release()
hands.close()
cv2.destroyAllWindows()

print("\nFinal text:")
print(text)

if text.strip():
    engine.say(text)
    engine.runAndWait()