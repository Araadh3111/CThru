import cv2
import time
import random
from collections import Counter
import HandTrackingModule as htm

FONT = cv2.FONT_HERSHEY_SIMPLEX
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (0, 0, 255)
YELLOW = (0, 255, 255)

moves = ["Rock", "Paper", "Scissors"]
beats = {"Rock": "Scissors", "Paper": "Rock", "Scissors": "Paper"}  # key beats value


def get_move(fingers):
    up = fingers[1:]  # ignore the thumb, its detection is unreliable
    if sum(up) == 0:
        return "Rock"
    if sum(up) == 4:
        return "Paper"
    if up == [1, 1, 0, 0]:
        return "Scissors"
    return None


def center_text(img, text, y, scale, color, thickness):
    size = cv2.getTextSize(text, FONT, scale, thickness)[0]
    x = (img.shape[1] - size[0]) // 2
    cv2.putText(img, text, (x, y), FONT, scale, color, thickness)


cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = htm.handDetector(detectionCon=0.8)

playerScore = 0
aiScore = 0

state = "waiting"  # waiting -> countdown -> result -> waiting
countdownStart = 0
resultStart = 0
recentMoves = []
playerMove = None
aiMove = ""
resultText = ""
resultColor = WHITE
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

    move = None
    if len(lmList) != 0:
        move = get_move(detector.fingersUP())

    # scoreboard
    cv2.rectangle(img, (440, 10), (840, 80), (40, 40, 40), cv2.FILLED)
    center_text(img, f"YOU {playerScore}  -  {aiScore} AI", 60, 1.4, WHITE, 3)

    # what the camera thinks you're showing right now
    if move:
        cv2.putText(img, f"You: {move}", (30, 690), FONT, 1.2, YELLOW, 3)

    if state == "waiting":
        center_text(img, "Press SPACE to play", 380, 1.6, WHITE, 4)

    elif state == "countdown":
        left = 3 - int(time.time() - countdownStart)
        if move:
            recentMoves.append(move)

        if left > 0:
            center_text(img, str(left), 420, 7, YELLOW, 14)
        else:
            # use the move seen most in the last few frames, one frame can glitch
            last = recentMoves[-8:]
            if last:
                playerMove = Counter(last).most_common(1)[0][0]
            else:
                playerMove = None

            aiMove = random.choice(moves)

            if playerMove is None:
                resultText = "No hand seen!"
                resultColor = WHITE
            elif playerMove == aiMove:
                resultText = "Draw"
                resultColor = YELLOW
            elif beats[playerMove] == aiMove:
                resultText = "You win!"
                resultColor = GREEN
                playerScore += 1
            else:
                resultText = "AI wins!"
                resultColor = RED
                aiScore += 1

            state = "result"
            resultStart = time.time()

    elif state == "result":
        center_text(img, resultText, 260, 3, resultColor, 7)
        if playerMove:
            center_text(img, f"{playerMove}  vs  {aiMove}", 360, 1.6, WHITE, 4)
        else:
            center_text(img, f"AI played {aiMove}", 360, 1.6, WHITE, 4)

        if time.time() - resultStart > 3:
            state = "waiting"

    cv2.putText(img, "SPACE: play | R: reset score | Q: quit", (820, 700), FONT, 0.6, WHITE, 2)
    cv2.imshow("Rock Paper Scissors", img)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    if key == ord(' ') and state == "waiting":
        state = "countdown"
        countdownStart = time.time()
        recentMoves = []
    if key == ord('r'):
        playerScore = 0
        aiScore = 0

cap.release()
cv2.destroyAllWindows()