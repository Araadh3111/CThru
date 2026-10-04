import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

dataset = pd.read_csv("dataset_hand_data.csv", header=None)
webcam = pd.read_csv("webcam_data.csv",header=None)

data = pd.concat([dataset,webcam],ignore_index=True)

X = data.iloc[:,1:]
y = data.iloc[:,0]

print("Total Samples:", len(data))
print("\nClass Count:")
print(y.value_counts())
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
print("\nModel accuracy", accuracy*100, "%")
with open("model_webcam.pkl","wb") as f:
    pickle.dump(model,f)

print("new model saved as model_webcam.pkl")