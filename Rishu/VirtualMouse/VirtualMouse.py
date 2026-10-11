import cv2 as cv
import mediapipe as mp
import time
import autopy

widthCam , heightCam = 640 , 480


cap = cv.VideoCapture(0)

while True:
    #1 find landmarks
    success, img = cap.read()

    #2 get tip of fingers(middle and index)
    #3 check which fingers are up
    #4 only index finger: moving mode
    #5 cvt coords to match video cam to screen
    #6 smoothen the values
    #7 move mouse
    #8 check for clicking mode (when both fingers are up)(stops moving)
    #9 find distance between fingers
    #10 click mouse if distance short
    #11 frame rate display
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv.putText(img,str(int(fps)),(20,70),cv.FONT_HERSHEY_PLAIN)
    #12 display
    cv.imshow("Image", img)
    cv.waitKey(1)