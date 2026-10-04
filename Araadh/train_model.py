import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

# Load dataset
data = pd.read_csv("dataset_hand_data.csv", header=None)

# Separate features and labels
X = data.iloc[:, 1:]
y = data.iloc[:, 0]

# Convert to copy
X = X.copy()

# Normalize hand size
for index in X.index:

    row = X.loc[index].to_numpy(copy=True)

    # Find maximum distance from wrist
    hand_size = 0

    for i in range(0, 63, 3):

        distance = (
            row[i] ** 2 +
            row[i + 1] ** 2 +
            row[i + 2] ** 2
        ) ** 0.5

        if distance > hand_size:
            hand_size = distance

    # Scale hand to same size
    if hand_size > 0:

        for i in range(63):
            row[i] /= hand_size

    X.loc[index] = row


print(X.iloc[0, :6])
print("Normalization complete!")


# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# Create model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)


# Train
model.fit(X_train, y_train)


# Test
predictions = model.predict(X_test)
cm = confusion_matrix(y_test, predictions, labels=model.classes_)
disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=model.classes_
)
disp.plot(xticks_rotation="vertical")
plt.tight_layout()
plt.show()

accuracy = accuracy_score(
    y_test,
    predictions
)

print(f"Model accuracy: {accuracy * 100:.2f}%")


# Save model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model saved successfully!")

# Show number of samples per letter
print(y.value_counts())