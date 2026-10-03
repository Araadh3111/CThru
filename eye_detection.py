# Detects Eye Position
import numpy as np
import cv2 as cv
cap = cv.VideoCapture(0)

while True:
    ret, frame = cap.read()
    width = int(cap.get(3))
    height = int(cap.get(4))
    
    cv.imshow('OpenCV',img)
    if cv.waitKey(1) == ord("q"):
        break
cap.release()
cv.destroyAllWindows()