import cv2
import numpy as np
import os
import HandTrackingModule as htm

brushThickness = 15
eraserThickness = 65

folderPath = "images"

# sorted so 1.jpg, 2.jpg, 3.jpg, 4.jpg load in the right order
# and only image files, so .DS_Store or folders dont break it
myList = sorted(os.listdir(folderPath))
myList = [f for f in myList if f.lower().endswith((".jpg", ".jpeg", ".png"))]
print(myList)

overLayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    image = cv2.resize(image, (1280, 125))
    overLayList.append(image)
print(len(overLayList))

header = overLayList[0]
drawColor = (255, 0, 255)

# transparency: 1.0 = solid, 0.1 = very see-through
alpha = 1.0

# slider position on the right side of the screen
sliderX1, sliderX2 = 1200, 1240
sliderTop, sliderBottom = 175, 625

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = htm.handDetector(detectionCon=0.85)
xp, yp = 0, 0

# imgCanvas stores the colours, alphaMap stores how see-through each pixel is
imgCanvas = np.zeros((720, 1280, 3), np.uint8)
alphaMap = np.zeros((720, 1280), np.float32)

fails = 0

while True:
    success, img = cap.read()

    if not success:
        fails += 1
        if fails > 30:
            print("camera not giving frames - is another program using it?")
            break
        continue
    fails = 0

    img = cv2.flip(img, 1)
    img = cv2.resize(img, (1280, 720))

    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]   # index finger tip
        x2, y2 = lmList[12][1:]  # middle finger tip

        fingers = detector.fingersUP()

        # selection mode - index and middle finger up
        if fingers[1] and fingers[2]:
            xp, yp = 0, 0

            # picking a colour from the header
            if y1 < 125:
                if 250 < x1 < 450:
                    header = overLayList[0]
                    drawColor = (255, 0, 255)
                elif 550 < x1 < 750:
                    header = overLayList[1]
                    drawColor = (255, 0, 0)
                elif 800 < x1 < 950:
                    header = overLayList[2]
                    drawColor = (0, 255, 0)
                elif 1050 < x1 < 1200:
                    header = overLayList[3]
                    drawColor = (0, 0, 0)

            # changing transparency with the slider
            if x1 > sliderX1 - 40 and sliderTop < y1 < sliderBottom:
                alpha = np.interp(y1, [sliderTop, sliderBottom], [1.0, 0.1])

            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)

        # drawing mode - only index finger up
        if fingers[1] and not fingers[2]:
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)

            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            if drawColor == (0, 0, 0):
                # eraser removes both the colour and the transparency
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
                cv2.line(alphaMap, (xp, yp), (x1, y1), 0, eraserThickness)
            else:
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(alphaMap, (xp, yp), (x1, y1), float(alpha), brushThickness)

            xp, yp = x1, y1

    # blend the drawing onto the webcam image using each pixel's transparency
    a = alphaMap[:, :, np.newaxis]
    img = (img * (1 - a) + imgCanvas * a).astype(np.uint8)

    img[0:125, 0:1280] = header

    # draw the slider
    if drawColor == (0, 0, 0):
        sliderColor = (255, 255, 255)
    else:
        sliderColor = drawColor
    level = int(np.interp(alpha, [0.1, 1.0], [sliderBottom, sliderTop]))
    cv2.rectangle(img, (sliderX1, sliderTop), (sliderX2, sliderBottom), (255, 255, 255), 2)
    cv2.rectangle(img, (sliderX1, level), (sliderX2, sliderBottom), sliderColor, cv2.FILLED)
    cv2.putText(img, f'{int(alpha * 100)}%', (sliderX1 - 15, sliderBottom + 35),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.imshow("Virtual Painter", img)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    if key == ord('c'):
        imgCanvas = np.zeros((720, 1280, 3), np.uint8)
        alphaMap = np.zeros((720, 1280), np.float32)
    if key == ord('+') or key == ord('='):
        alpha = min(1.0, alpha + 0.1)
    if key == ord('-'):
        alpha = max(0.1, alpha - 0.1)

cap.release()
cv2.destroyAllWindows()