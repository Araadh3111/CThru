import cv2
import numpy as np
import time
import os
import HandTrackingModule as htm

brushThickness = 15
eraserThickness = 65

folderPath = "images"
myList = os.listdir(folderPath)
print(myList)
overLayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overLayList.append(image)
print(len(overLayList))

header = overLayList[0]
drawColor = (255,0,255)

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

detector = htm.handDetector(detectionCon=0.85)
xp,yp = 0,0
imgCanvas = np.zeros((720,1280, 3), np.uint8)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    
    if len(lmList)!=0:
        #print(lmList)
        
        x1,y1 = lmList[8][1:]
        x2,y2 = lmList[12][1:]

        fingers = detector.fingersUP()
        print(fingers)

        if fingers[1] and fingers[2]:
            xp,yp = 0,0
            if y1<125:
                if 250<x1<450:
                    images = overLayList[0]
                    drawColor = (255,0,255)
                elif 550<x1<750:
                    images = overLayList[1]
                    drawColor = (255,0,0)
                elif 800<x1<950:
                    images = overLayList[2]
                    drawColor = (0,255,0)
                elif 1050<x1<1200:
                    images = overLayList[3]
                    drawColor = (0,0,0)
            cv2.rectangle(img,(x1,y1-25), (x2,y2+15), drawColor, cv2.FILLED)

        if fingers[1] and fingers[2] == False:
            cv2.circle(img, (x1,y1),25 ,drawColor, cv2.FILLED)
            print("Drawing mode")
            if xp==0 and yp==0:
                xp,yp = x1,y1

            if drawColor == (0,0,0):
                cv2.line(img, (xp,yp),(x1,y1), drawColor, eraserThickness)
                cv2.line(imgCanvas, (xp,yp),(x1,y1), drawColor, eraserThickness)

            else:
                cv2.line(img, (xp,yp),(x1,y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp,yp),(x1,y1), drawColor, brushThickness)

            xp,yp = x1,y1

    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray,50,255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)

    img[0:125, 0:1280] = header
    #img = cv2.addWeighted(img,0.5, imgCanvas, 0.5,0)
    cv2.imshow("Image", img)
    cv2.imshow("Canvas", imgCanvas)
    cv2.imshow("Inv", imgInv)
    cv2.waitKey(1)