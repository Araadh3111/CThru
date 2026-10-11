import os
import sys
import queue
import struct
import threading
import runpy
import cv2

script = os.path.abspath(sys.argv[1])

frameOut = os.fdopen(os.dup(1), "wb")
os.dup2(2, 1)
sys.stdout = sys.stderr

keys = queue.Queue()


def read_keys():
    for line in sys.stdin:
        line = line.rstrip("\n")
        if line:
            keys.put(line[0])
    keys.put(None)  


threading.Thread(target=read_keys, daemon=True).start()

mainWindow = None


def imshow(name, img):
    global mainWindow
    if mainWindow is None:
        mainWindow = name
    if name != mainWindow or img is None:
        return

    ok, buffer = cv2.imencode(".jpg", img, [cv2.IMWRITE_JPEG_QUALITY, 75])
    if not ok:
        return
    data = buffer.tobytes()
    try:
        frameOut.write(struct.pack(">I", len(data)) + data)
        frameOut.flush()
    except BrokenPipeError:
        os._exit(0)


def waitKey(delay=0):
    try:
        if delay <= 0:
            key = keys.get()
        else:
            key = keys.get(timeout=delay / 1000)
    except queue.Empty:
        return -1
    if key is None:
        os._exit(0)
    return ord(key)


def nothing(*args, **kwargs):
    return None


cv2.imshow = imshow
cv2.waitKey = waitKey
cv2.waitKeyEx = waitKey
cv2.namedWindow = nothing
cv2.destroyAllWindows = nothing
cv2.destroyWindow = nothing
cv2.moveWindow = nothing
cv2.resizeWindow = nothing
cv2.setMouseCallback = nothing
cv2.setWindowProperty = nothing

sys.argv = [script]
sys.path.insert(0, os.path.dirname(script))
runpy.run_path(script, run_name="__main__")