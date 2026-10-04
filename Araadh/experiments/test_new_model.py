import pandas as pd
import pickle

with open("model_webcam.pkl","rb") as f:
    model = pickle.load(f)

data = pd.read_csv("webcam_data.csv",header=None)

X = data.iloc[:,1:]

predictions = model.predict(X)

correct = 0
for prediction in predictions:
    if prediction=='D':
        correct+=1

print("correct D preds:", correct, "/100")
print("accuracy:", correct, "%")