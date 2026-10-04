import cv2
import os 

SAMPLES = 800
LABEL = "backspace"

SAVE_PATH =  f"../asl_dataset/asl_alphabet_train/asl_alphabet_train/{LABEL}"

os.makedirs(SAVE_PATH,exist_ok=True)

cam = cv2.VideoCapture(0)
count = 0
print(f"\nCollecting: {LABEL}")
print("press space to start collecting")
print("press q to quit")
started = False
while True:
    success,frame = cam.read()
    if not success:
        print("cam not working")
        break

    frame = cv2.flip(frame,1)

    if started and count < SAMPLES:
        filename = os.path.join(
            SAVE_PATH,
            f"{LABEL}_{count}.jpg"
        )

        cv2.imwrite(filename,frame)
        count+=1


    cv2.putText(
        frame,
        f"{LABEL}: {count}/{SAMPLES}",
        (30,50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0,255,0),
        2
    )

    cv2.imshow("Cthru-datacollection", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord(" "):
        started=True

    if key == ord("q"):
        break

    if count>=SAMPLES:
        print(f"finished collecting {LABEL}")
        break


cam.release()
cv2.destroyAllWindows()
print(f"\nSved {count} images to:")
print(SAVE_PATH)