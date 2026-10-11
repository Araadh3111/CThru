import cv2
import math
import numpy as np
import mediapipe as mp

mpPose = mp.solutions.pose
mpDraw = mp.solutions.drawing_utils
pose = mpPose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7)


def get_angle(a, b, c):
    angle = math.degrees(math.atan2(c[1] - b[1], c[0] - b[0]) -
    math.atan2(a[1] - b[1], a[0] - b[0]))

    angle = abs(angle)
    if angle > 180:
        angle = 360 - angle
    return angle

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

count = 0
stage = "down"

while True:
    success, img = cap.read()
    if not success:
        break
    img = cv2.flip(img, 1)
    h, w, _ = img.shape

    results = pose.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        lm = results.pose_landmarks.landmark

        def point(i):
            return int(lm[i].x * w), int(lm[i].y * h)

        angle1 = get_angle(point(11), point(13), point(15))
        angle2 = get_angle(point(12), point(14), point(16))

        if angle1 < angle2:
            angle, elbow = angle1, point(13)
        else:
            angle, elbow = angle2, point(14)

        if angle > 150:
            stage = "down"
        if angle < 50 and stage == "down":
            stage = "up"
            count += 1

        cv2.putText(img, str(int(angle)), (elbow[0] + 20, elbow[1]),
        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)

        per = np.interp(angle, [50, 150], [100, 0])
        bar = np.interp(angle, [50, 150], [150, 550])
        color = (0, 255, 0) if per == 100 else (255, 0, 255)
        cv2.rectangle(img, (1150, 150), (1200, 550), color, 3)
        cv2.rectangle(img, (1150, int(bar)), (1200, 550), color, cv2.FILLED)
        cv2.putText(img, f'{int(per)}%', (1130, 600), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 3)


    cv2.rectangle(img, (0, 0), (260, 130), (40, 40, 40), cv2.FILLED)
    cv2.putText(img, "REPS", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 2.5, (255, 255, 255), 5)
    cv2.putText(img, str(count), (20, 115), cv2.FONT_HERSHEY_SIMPLEX, 2.5, (255, 255, 255), 5)
    cv2.putText(img, stage.upper(), (140, 115), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    cv2.imshow("Curl Counter", img)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break
    if key == ord('r'):
        count = 0

cap.release()
cv2.destroyAllWindows()