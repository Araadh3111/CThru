import pandas as pd
import pickle

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

webcam = pd.read_csv("webcam_data.csv", header=None)

X_webcam = webcam.iloc[:, 1:].copy()

dataset = pd.read_csv("dataset_hand_data.csv", header=None)

X_dataset = dataset[dataset.iloc[:, 0] == "D"].iloc[:, 1:]

predictions = model.predict(X_webcam)

print("Webcam D predictions:")
print(pd.Series(predictions).value_counts())

print("\nNumber of D samples in original dataset:", len(X_dataset))

print("\nFirst webcam D:")
print(X_webcam.iloc[0, :9].to_numpy())

print("\nFirst Dataset D:")
print(X_dataset.iloc[0, :9].to_numpy())