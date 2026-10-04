import time

last_prediction = None
same_count = 0
required_count = 5

while True:
    prediction = input("prediction:  ")

    if prediction == last_prediction:
        same_count+=1

    else:
        last_prediction= prediction
        same_count=1

    if same_count>=required_count:
        print("confirmed:", prediction)
        same_count=0
        last_prediction=None