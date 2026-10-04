from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
import pickle
import mediapipe as mp

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

with open("models/model_webcam.pkl", "rb") as f:
    model = pickle.load(f)

mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7
)

text = ""

locked_prediction = None
last_prediction = None
prediction_count = 0
required_count = 8


@app.post("/predict")
async def predict(request: Request):

    global text
    global locked_prediction
    global last_prediction
    global prediction_count

    image_data = await request.body()

    image_array = np.frombuffer(image_data, np.uint8)

    frame = cv2.imdecode(
        image_array,
        cv2.IMREAD_COLOR
    )

    rgb = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    result = hands.process(rgb)

    if not result.multi_hand_landmarks:

        prediction_count = 0
        last_prediction = None
        locked_prediction = None

        return {
            "sign": "None",
            "confidence": 0,
            "text": text
        }

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

    # Stability tracking

    if prediction == last_prediction:

        prediction_count += 1

    else:

        last_prediction = prediction
        prediction_count = 1

    # Confirm prediction

    if prediction_count >= required_count:

        if prediction != locked_prediction:

            if prediction == "space":

                text += " "

            elif prediction == "backspace":

                text = text[:-1]

            elif prediction == "clear":

                text = ""

            else:

                text += prediction

            locked_prediction = prediction

            prediction_count = 0

    return {
        "sign": prediction,
        "confidence": round(confidence, 1),
        "text": text
    }