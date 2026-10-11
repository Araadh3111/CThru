import cv2
import numpy as np
import time
import math
import HandTrackingModule as htm

GREEN = (0, 255, 0)


def detect_shape(points):
    # works on the actual path the finger took, not the drawn pixels
    pts = np.array(points, dtype=np.int32)
    result = np.zeros((720, 1280, 3), dtype=np.uint8)

    x, y, w, h = cv2.boundingRect(pts)
    labelPos = (x, max(40, y - 20))
    size = math.hypot(w, h)

    if len(pts) < 10 or size < 100:
        return "Too small", result, labelPos

    contour = pts.reshape(-1, 1, 2)

    # if the start and end are far apart, check if it's just a straight line
    gap = math.hypot(pts[0][0] - pts[-1][0], pts[0][1] - pts[-1][1])
    if gap > 0.4 * size:
        openApprox = cv2.approxPolyDP(contour, 0.05 * cv2.arcLength(contour, False), False)
        if len(openApprox) == 2:
            cv2.line(result, tuple(map(int, pts[0])), tuple(map(int, pts[-1])), GREEN, 8)
            return "Line", result, labelPos

    # convex hull = the shape with all the hand-shake wobbles smoothed out
    hull = cv2.convexHull(contour)
    peri = cv2.arcLength(hull, True)
    area = cv2.contourArea(hull)
    # 1.0 for a perfect circle, about 0.78 for a square, about 0.6 for a triangle
    circularity = 4 * math.pi * area / (peri * peri)

    approx = cv2.approxPolyDP(hull, 0.04 * peri, True)
    corners = len(approx)

    if corners == 3:
        cv2.polylines(result, [approx], True, GREEN, 8)
        return "Triangle", result, labelPos

    # how much of its tightest box the shape fills: rectangle is about 1.0, oval about 0.79
    rect = cv2.minAreaRect(hull)
    rw, rh = rect[1]
    fill = area / (rw * rh) if rw * rh > 0 else 0

    if corners == 4 and fill > 0.85:
        box = np.int32(cv2.boxPoints(rect))
        cv2.polylines(result, [box], True, GREEN, 8)
        if 0.8 < rw / rh < 1.25:
            return "Square", result, labelPos
        return "Rectangle", result, labelPos

    # everything else is round-ish, so fit an ellipse to it
    ellipse = cv2.fitEllipse(hull)
    ew, eh = ellipse[1]
    roundness = min(ew, eh) / max(ew, eh)  # 1.0 = circle, smaller = more stretched

    if corners == 5 and roundness > 0.75 and circularity < 0.92:
        cv2.polylines(result, [approx], True, GREEN, 8)
        return "Pentagon", result, labelPos

    if roundness < 0.75:
        cv2.ellipse(result, ellipse, GREEN, 8)
        return "Oval", result, labelPos

    (cx, cy), r = cv2.minEnclosingCircle(hull)
    cv2.circle(result, (int(cx), int(cy)), int(r), GREEN, 8)
    return "Circle", result, labelPos


if __name__ == "__main__":
    detector = htm.handDetector(detectionCon=0.85)

    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    canvas = np.zeros((720, 1280, 3), dtype=np.uint8)
    points = []  # every point drawn, in order. used to work out the shape

    xp, yp = 0, 0  # previous point, for drawing lines
    sx, sy = 0, 0  # smoothed fingertip position
    smoothing = 0.5  # 0 = no smoothing, closer to 1 = smoother but more lag

    fistFrames = 0  # how many frames in a row the fist has been held
    FIST_HOLD = 6

    resultText = ""
    resultImg = None
    labelPos = (0, 0)
    resultUntil = 0

    mode = ""
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

        showingResult = time.time() < resultUntil

        # result finished showing -> clear everything for the next shape
        if resultUntil != 0 and not showingResult:
            canvas = np.zeros((720, 1280, 3), dtype=np.uint8)
            points = []
            resultUntil = 0

        if len(lmList) != 0 and not showingResult:
            x1, y1 = lmList[8][1], lmList[8][2]

            # smooth the shaky fingertip so lines dont get extra corners
            if sx == 0 and sy == 0:
                sx, sy = x1, y1
            sx = int(smoothing * sx + (1 - smoothing) * x1)
            sy = int(smoothing * sy + (1 - smoothing) * y1)

            fingers = detector.fingersUP()

            # fist = all 4 fingers down. thumb is ignored, its detection is unreliable
            if sum(fingers[1:]) == 0:
                fistFrames += 1
                xp, yp = 0, 0
                mode = "Hold fist..."

                # only detect after the fist is held for a few frames, not on a random blip
                if fistFrames == FIST_HOLD and len(points) > 0:
                    resultText, resultImg, labelPos = detect_shape(points)
                    resultUntil = time.time() + 2.5
            else:
                fistFrames = 0

                if fingers[1] and fingers[2]:
                    xp, yp = 0, 0
                    mode = "Pen up"

                elif fingers[1]:
                    mode = "Drawing"
                    if xp == 0 and yp == 0:
                        xp, yp = sx, sy
                        points.append((sx, sy))

                    # skip tiny movements, they are just hand shake
                    if math.hypot(sx - xp, sy - yp) > 4:
                        cv2.line(canvas, (xp, yp), (sx, sy), (255, 255, 255), 12)
                        points.append((sx, sy))
                        xp, yp = sx, sy

            cv2.circle(img, (sx, sy), 10, (255, 0, 255), cv2.FILLED)

        elif len(lmList) == 0:
            # hand left the screen - dont draw a line from where it left to where it comes back
            xp, yp = 0, 0
            sx, sy = 0, 0
            fistFrames = 0

        if showingResult:
            img = cv2.addWeighted(img, 1, canvas, 0.3, 0)  # faded hand drawing
            img = cv2.add(img, resultImg)  # clean shape on top
            cv2.putText(img, resultText, labelPos, cv2.FONT_HERSHEY_SIMPLEX, 1.6, GREEN, 4)
        else:
            img = cv2.add(img, canvas)

        cv2.putText(img, mode, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
        cv2.putText(img, "Index: draw | 2 fingers: pen up | Fist: detect | C: clear | Q: quit",
                    (30, 700), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        cv2.imshow("Air Draw", img)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        if key == ord('c'):
            canvas = np.zeros((720, 1280, 3), dtype=np.uint8)
            points = []
            resultUntil = 0

    cap.release()
    cv2.destroyAllWindows()