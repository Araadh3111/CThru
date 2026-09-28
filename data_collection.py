import cv2
import mediapipe as mp
cam = cv2.VideoCapture(0)
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hand= mp_hands.Hands()
while True:
    rect,frame = cam.read()
    RGB_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    result = hand.process(RGB_frame)
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            print(hand_landmarks)
            mp_drawing.draw_landmarks(frame, hand_landmarks,mp_hands.HAND_CONNECTIONS)


    cv2.imshow('Hand Recognition',frame)

    if cv2.waitKey(1) == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()