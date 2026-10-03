import cv2
import numpy as np
import HandTrackingModule as htm

detector = htm.handDetector(detectionCon=0.85)

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

canvas = np.zeros((720, 1280, 3), dtype=np.uint8)

xp, yp = 0, 0

while True:
    success, img = cap.read()
    if not success:
        break
    img = cv2.flip(img, 1)

    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        x1, y1 = lmList[8][1], lmList[8][2]

        fingers = detector.fingersUP()

        # two fingers up = selection mode
        if fingers[1] and fingers[2]:
            xp, yp = 0, 0

        # only index finger up = drawing mode
        if fingers[1] and not fingers[2]:
            if xp == 0 and yp == 0:
                xp, yp = x1, y1
            cv2.line(canvas, (xp, yp), (x1, y1), (255, 255, 255), 15)
            xp, yp = x1, y1

        # fist = recognize shape
        if fingers.count(1) == 0:
            gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area > 1000:
                    peri = cv2.arcLength(cnt, True)
                    approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
                    corners = len(approx)

                    if corners == 3:
                        shape = "Triangle"
                    elif corners == 4:
                        shape = "Rectangle"
                    elif corners > 6:
                        shape = "Circle"
                    else:
                        shape = f"{corners}-gon"

                    x, y, w, h = cv2.boundingRect(approx)
                    cv2.putText(img, shape, (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            img = cv2.add(img, canvas)
            cv2.imshow("Air Draw", img)
            cv2.waitKey(2000)
            canvas = np.zeros((720, 1280, 3), dtype=np.uint8)
            xp, yp = 0, 0

    img = cv2.add(img, canvas)

    cv2.imshow("Air Draw", img)
    cv2.imshow("Canvas", canvas)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()