import cv2
import mediapipe as mp
import csv 
import os 
import random

DATASET_PATH = "asl_dataset/asl_alphabet_train/asl_alphabet_train"
OUTPUT_FILE = "dataset_hand_data.csv"

LETTERS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
SAMPLES_PER_LETTER = 1000
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode = True,
    max_num_hands = 1,
    min_detection_confidence = 0.5
)

with open(OUTPUT_FILE,"w",newline="") as f:
    writer = csv.writer(f)

    for letter in LETTERS:
        folder=os.path.join(DATASET_PATH,letter)

        if not os.path.exists(folder):
            print(f"folder not found:  {letter}")
            continue

        images = os.listdir(folder)

        images = [
            x for x in images
            if x.lower().endswith((".jpg",".jpeg",".png"))
        ]

        random.shuffle(images)

        images = images[:SAMPLES_PER_LETTER]
        print(f"\nProcessing {letter}: {len(images)} images")

        saved = 0

        for image_name in images:
            image_path = os.path.join(folder,image_name)
            image = cv2.imread(image_path)

            if image is None:
                continue

            rgb = cv2.cvtColor(
                image,
                cv2.COLOR_BGR2RGB
            )

            result = hands.process(rgb)

            if not result.multi_hand_landmarks:
                continue
            hand_landmarks = result.multi_hand_landmarks[0]

            row_data = []

            for landmark in hand_landmarks.landmark:
                row_data.extend([
                    landmark.x,
                    landmark.y,
                    landmark.z
                ])


            wrist_x = row_data[0]
            wrist_y = row_data[1]
            wrist_z = row_data[2]

            for i in range(0,63,3):
                row_data[i]-=wrist_x
                row_data[i+1] -= wrist_y
                row_data[i+2]-=wrist_z

            hand_size = 0

            for i in range(0,63,3):

                distance = (
                    row_data[i] ** 2 +
                    row_data[i+1]**2+
                    row_data[i+2]**2
                )**0.5

                if distance > hand_size:
                    hand_size=distance


            if hand_size>0:
                for i in range(63):
                    row_data[i] /= hand_size

            row_data.insert(0,letter)

            writer.writerow(row_data)

            saved+=1

        print(f"saved {letter}: {saved}")

hands.close()
print("\nDone!")
print(f"dataset saved to:  {OUTPUT_FILE}")
