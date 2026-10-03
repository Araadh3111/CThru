#Detects Color and Displays Color Specified by the User
import numpy as np
import cv2 as cv
cap = cv.VideoCapture(0)

while True:
    ret, frame = cap.read()
    width = int(cap.get(3))
    height = int(cap.get(4))

    hsv = cv.cvtColor(frame,cv.COLOR_BGR2HSV)
    lower_blue = np.array([90,50,50])
    upper_blue = np.array([135,255,255])

    mask = cv.inRange(hsv,lower_blue,upper_blue)
    result = cv.bitwise_and(frame,frame, mask=mask)
    
    
    cv.imshow('OpenCV',result) 
    cv.imshow('Mask',mask)

#Exit Key - "X"
    if cv.waitKey(1) == ord("q"):
        break
cap.release()
cv.destroyAllWindows()