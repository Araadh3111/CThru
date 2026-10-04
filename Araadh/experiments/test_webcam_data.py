import pandas as pd
import pickle

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

data = pd.read_csv("webcam_data.csv", header=None)

X = data.iloc[:, 1:].copy()

# Same normalization used in train_model.py
for index in X.index:
    row = X.loc[index].to_numpy(copy=True)

    hand_size = 0

    for i in range(0, 63, 3):
        distance = (
            row[i] ** 2 +
            row[i + 1] ** 2 +
            row[i + 2] ** 2
        ) ** 0.5

        if distance > hand_size:
            hand_size = distance

    if hand_size > 0:
        for i in range(63):
            row[i] /= hand_size

    X.loc[index] = row

predictions = model.predict(X)
print(pd.Series(predictions).value_counts())
correct = 0

for prediction in predictions:
    if prediction == "D":
        correct += 1

print("Correct D predictions:", correct, "/ 100")
print("Accuracy:", correct, "%")