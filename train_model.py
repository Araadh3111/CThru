import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle
data = pd.read_csv("dataset_hand_data.csv", header=None)


X = data.iloc[:, 1:]
y = data.iloc[:, 0]


X = X.copy()

for index in X.index:
    row = X.loc[index].to_numpy(copy=True)

    wrist_x = row[0]
    wrist_y = row[1]
    wrist_z = row[2]

    for i in range(0, 63, 3):
        row[i] -= wrist_x
        row[i + 1] -= wrist_y
        row[i + 2] -= wrist_z

    X.loc[index] = row


print(X.iloc[0, :6])
print("Normalization complete!")


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)
model.fit(X_train,y_train)
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test,predictions)
print(f"model accuracy: {accuracy*100:.2f}%")
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model saved successfully!")
print(y.value_counts())