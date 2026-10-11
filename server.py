import os
import sys
import time
import struct
import threading
import subprocess

from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)
RUNNER = os.path.join(ROOT, "runner.py")

from api.index import predict

PROGRAMS = {
    "shape": ("Shape Detector", "Siddak", "siddakjr", "shape_detection.py"),
    "painter": ("Virtual Painter", "Siddak", "siddakjr", "VirtualPainter.py"),
    "volume": ("Volume Control", "Siddak", "siddakjr", "VolumeHandControl.py"),
    "fingers": ("Finger Counter", "Siddak", "siddakjr", "FingerCounter.py"),
    "blur": ("Face Blur", "Siddak", "siddakjr", "face_blurring.py"),
    "rps": ("Rock Paper Scissors", "Siddak", "siddakjr", "RockPaperScissors.py"),
    "curls": ("Curl Counter", "Siddak", "siddakjr", "CurlCounter.py"),

    "sign": ("Sign Language (desktop)", "Araadh", ".", "Araadh/recognize_words.py"),

    "hands": ("Hand Tracking", "Rishu", "Rishu/handTracking", "HTmodule.py"),
    "pose": ("Pose Estimation", "Rishu", "Rishu/poseEstimation", "PEmodule.py"),
    "facedetect": ("Face Detection", "Rishu", "Rishu/faceDetection", "FDmodule.py"),
    "facemesh": ("Face Mesh", "Rishu", "Rishu/faceMesh", "FMmodule.py"),
    "facetracker": ("Face + Eye Tracker", "Rishu", "Rishu/TrainingWheels", "facial_tracker.py"),
    "color": ("Color Displayer", "Rishu", "Rishu", "color_displayer.py"),
    "corners": ("Corner Detection", "Rishu", "Rishu", "TrainingWheels/corner_detection.py"),
}

app = FastAPI()
app.add_api_route("/api/predict", predict, methods=["POST"])

running = None    
runningId = None
runNumber = 0      
latestFrame = None
frameNumber = 0


def is_running():
    return running is not None and running.poll() is None


def read_frames(proc, myRun):
    global latestFrame, frameNumber
    while runNumber == myRun:
        header = proc.stdout.read(4)
        if len(header) < 4:
            break
        size = struct.unpack(">I", header)[0]
        data = proc.stdout.read(size)
        if len(data) < size:
            break
        latestFrame = data
        frameNumber += 1


def stop_current():
    global running, runningId, latestFrame
    if is_running():
        running.terminate()
        try:
            running.wait(timeout=3)
        except subprocess.TimeoutExpired:
            running.kill()
    running = None
    runningId = None
    latestFrame = None


@app.get("/api/programs")
def list_programs():
    result = []
    for pid, (name, member, folder, file) in PROGRAMS.items():
        result.append({
            "id": pid,
            "name": name,
            "member": member,
            "ready": os.path.exists(os.path.join(ROOT, folder, file)),
        })
    return result


@app.post("/api/start/{pid}")
def start_program(pid: str):
    global running, runningId, runNumber

    if pid not in PROGRAMS:
        return {"ok": False, "error": "Unknown program"}

    name, member, folder, file = PROGRAMS[pid]
    if not os.path.exists(os.path.join(ROOT, folder, file)):
        return {"ok": False, "error": file + " not found"}

    stop_current()
    runNumber += 1

    running = subprocess.Popen(
        [sys.executable, RUNNER, file],
        cwd=os.path.join(ROOT, folder),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )
    runningId = pid
    threading.Thread(target=read_frames, args=(running, runNumber), daemon=True).start()
    return {"ok": True, "running": name}


@app.post("/api/stop")
def stop_program():
    global runNumber
    runNumber += 1
    stop_current()
    return {"ok": True}


@app.post("/api/key")
async def send_key(request: Request):
    data = await request.json()
    key = str(data.get("key", ""))[:1]
    if key and is_running():
        try:
            running.stdin.write((key + "\n").encode())
            running.stdin.flush()
        except BrokenPipeError:
            pass
    return {"ok": True}


@app.get("/api/status")
def status():
    if is_running():
        return {"running": PROGRAMS[runningId][0], "id": runningId}
    return {"running": None, "id": None}


@app.get("/video")
def video():
    myRun = runNumber

    def frames():
        lastFrame = -1
        lastSent = 0
        while runNumber == myRun and is_running():
            if latestFrame is not None and (frameNumber != lastFrame or time.time() - lastSent > 0.5):
                frame = latestFrame
                lastFrame = frameNumber
                lastSent = time.time()
                yield (b"--frame\r\nContent-Type: image/jpeg\r\nContent-Length: " +
                       str(len(frame)).encode() + b"\r\n\r\n" + frame + b"\r\n")
            else:
                time.sleep(0.01)

    return StreamingResponse(frames(), media_type="multipart/x-mixed-replace; boundary=frame")


app.mount("/", StaticFiles(directory=ROOT, html=True), name="site")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)