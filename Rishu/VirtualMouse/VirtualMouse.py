import cv2 as cv
import mediapipe as mp
import numpy as np
import HTmodule as htm
import time
import autopy

widthCam , heightCam = 640 , 480
frameR = 100 #frame reduction
smoothening = 7
widthScreen ,heightScreen = autopy.screen.size()
#print(widthScreen,heightScreen)

pLocX,pLocY = 0,0
cLocX,cLocY = 0,0


cap = cv.VideoCapture(0)
cap.set(3,widthCam)
cap.set(4,heightCam)
pTime = 0 
detector = htm.handDetector(maxHands = 1)

while True:
    #1 find landmarks
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img)
    cv.rectangle(img,(frameR,frameR),(widthCam-frameR, heightCam-frameR),(255,0,255),2)
    #2 get tip of fingers(middle and index)
    if len(lmList) != 0:
        x1,y1 = lmList[8][1:]
        x2,y2 = lmList[12][1:]
        #print(x1,y1,x2,y2)


    #3 check which fingers are up
        fingers = detector.fingersUp()
    #print(fingers)
    #4 only index finger: moving mode
        if fingers[1] == 1 and fingers[2] == 0:
    #5 cvt coords to match video cam to screen
            x3 = np.interp(x1,(frameR,widthCam-frameR),(0,widthScreen))
            y3 = np.interp(y1,(frameR,heightCam-frameR),(0,heightScreen))
    #6 smoothen the values
            cLocX = pLocX + (x3 - pLocX) /smoothening
            cLocY = pLocY + (y3 - pLocY) /smoothening
    #7 move mouse
            autopy.mouse.move(widthScreen-cLocX,cLocY)
            cv.circle(img,(x1,y1),15,(255,0,255),cv.FILLED)
            pLocX,pLocY = cLocX,cLocY
    #8 find distance between fingers and click if distance is less than 40 units
        if fingers[1] == 1 and fingers[2] == 1:
            length,img, lineInfo = detector.findDistance(8,12,img)
            if length < 40:
                cv.circle(img,(lineInfo[4],lineInfo[5]),15,(0,255,0),cv.FILLED)
                autopy.mouse.click()
    
    #9 frame rate display
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv.putText(img,str(int(fps)),(20,70),cv.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    #12 display
    cv.imshow("Image", img)
    cv.waitKey(1)