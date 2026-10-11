import math
import os
import subprocess
import sys
import time
import tkinter as tk
import tkinter.font
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageTk
import webbrowser
here = os.path.dirname(os.path.abspath(__file__))
main_folder = os.path.dirname(here)
assets = os.path.join(here, "assets")

W, H = 900, 640
font_choices = ["SF Pro Display", "SF Pro Text", "SF Pro", "Segoe UI", "Helvetica Neue"]
font_name = "Segoe UI"

recolour = True
navy = np.array([6, 16, 54], np.float32)
purple = np.array([45, 30, 106], np.float32)
blue = np.array([10, 40, 72], np.float32)

scripts = {
    "Hand": "Rishu/handTracking/HTmodule.py",
    "Face Box": "Rishu/faceDetection/FDmodule.py",
    "Face Mesh": "Rishu/faceMesh/FMmodule.py",
    "Pose": "Rishu/poseEstimation/PEmodule.py",
    "ASL": "https://cthru.vercel.app/",
    "Face Blur": "siddakjr/face_blurring.py",
    "Finger Count": "siddakjr/FingerCounter.py",
    "Virtual Painter": "siddakjr/VirtualPainter.py",
    "Volume Control": "siddakjr/VolumeHandControl.py",
    "Shape Detector": "siddakjr/shape_detection.py",
}

headings = [
    ("Modules", 450, 74, 156),
    ("Sign language", 113, 319, 200),
    ("Misc", 513, 587, 156),
]

buttons = [
    ("Hand", 273, 133),
    ("Face Box", 628, 133),
    ("Face Mesh", 332, 202),
    ("Pose", 569, 202),
    ("ASL", 106, 393),
    ("Face Blur", 395, 437),
    ("Finger Count", 630, 437),
    ("Virtual Painter", 332, 512),
    ("Volume Control", 513, 512),
    ("Shape Detector", 689, 512),
]

lines = [
    (451, 133, 451, 272),
    (224, 321, 317, 321),
    (671, 321, 743, 321),
    (513, 370, 513, 464),
]

blobs = [
    (40, 30, 25, 22, (52, 28, 120), 0.50),
    (38, 64, 23, 16, (64, 34, 140), 0.35),
    (82, 0, 23, 15, (14, 52, 96), 0.42),
    (74, 36, 26, 20, (6, 12, 56), 0.30),
]

credits = [
    "Araadh  -  ASL sign language recognition(the hardest one thats why I am the goat)",
    "Siddak  -  Face Blur, Finger Count, Virtual Painter, Volume Control, Shape Detector",
    "Rishu  -  Hand, Face Box, Face Mesh, Pose",
]

running = None
status = None
images = []
started = time.time()
video = None
delay = 60

bg_file = None
for file_name in ("bg.mp4", "bg.gif", "bg.png"):
    if os.path.exists(os.path.join(assets, file_name)):
        bg_file = os.path.join(assets, file_name)
        break


def make_background(t):
    small = Image.new("RGB", (90, 64), (7, 13, 58))
    draw = ImageDraw.Draw(small)
    for cx, cy, rx, ry, colour, speed in blobs:
        x = cx + 10 * math.sin(t * speed)
        y = cy + 7 * math.cos(t * speed * 0.7)
        draw.ellipse((x - rx, y - ry, x + rx, y + ry), fill=colour)
    small = small.filter(ImageFilter.GaussianBlur(9))
    return small.resize((W, H), Image.BICUBIC)


def design_colours(frame):
    small = frame[::8, ::8].astype(np.float32)
    b = small[:, :, 0]
    g = small[:, :, 1]
    blue_part = np.clip(0.0157 * b - 0.0058 * g - 0.7988, 0, 1) ** 2.0
    purple_part = 1.1 * np.clip(0.0099 * g - 0.0148 * b + 0.6743, 0, 1) ** 1.3
    mixed = navy + purple_part[:, :, None] * (purple - navy) + blue_part[:, :, None] * (blue - navy)
    big = cv2.resize(mixed, (W, H), interpolation=cv2.INTER_CUBIC)
    return np.clip(big, 0, 255).astype(np.uint8)


def next_background():
    global video, delay
    if bg_file is None:
        return make_background(time.time() - started)
    if bg_file.endswith(".png"):
        return Image.open(bg_file).convert("RGB").resize((W, H))
    if video is None:
        video = cv2.VideoCapture(bg_file)
        fps = video.get(cv2.CAP_PROP_FPS)
        if fps > 0:
            delay = int(2000 / fps)
    video.grab()
    ok, frame = video.read()
    if not ok:
        video.release()
        video = cv2.VideoCapture(bg_file)
        ok, frame = video.read()
    if not ok:
        return make_background(time.time() - started)
    if recolour:
        return Image.fromarray(design_colours(frame))
    return Image.fromarray(cv2.cvtColor(cv2.resize(frame, (W, H)), cv2.COLOR_BGR2RGB))


def animate():
    began = time.time()
    if running is None:
        background.paste(next_background())
    if bg_file is None or not bg_file.endswith(".png"):
        spent = int((time.time() - began) * 1000)
        window.after(max(1, delay - spent), animate)


def rounded(w, h, radius, fill, outline, width):
    big = Image.new("RGBA", (w * 3, h * 3), (0, 0, 0, 0))
    draw = ImageDraw.Draw(big)
    draw.rounded_rectangle((0, 0, w * 3 - 1, h * 3 - 1), radius * 3, fill=fill, outline=outline, width=width * 3)
    return big.resize((w, h), Image.LANCZOS)


def eye_image(width, alpha=255):
    path = os.path.join(assets, "eye.png")
    if os.path.exists(path):
        eye = Image.open(path).convert("RGBA")
        eye = eye.resize((width, int(width * eye.height / eye.width)), Image.LANCZOS)
    else:
        w, h = width * 3, int(width * 2.4)
        eye = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(eye)
        draw.ellipse((4, int(h * 0.1), w - 4, int(h * 0.9)), fill=(238, 238, 246), outline=(12, 12, 40), width=w // 22)
        draw.ellipse((int(w * 0.5 - h * 0.3), int(h * 0.2), int(w * 0.5 + h * 0.3), int(h * 0.8)), fill=(38, 64, 165))
        draw.ellipse((int(w * 0.5 - h * 0.12), int(h * 0.38), int(w * 0.5 + h * 0.12), int(h * 0.62)), fill=(10, 14, 50))
        eye = eye.resize((width, int(width * 0.8)), Image.LANCZOS)
    if alpha < 255:
        eye.putalpha(eye.getchannel("A").point(lambda value: value * alpha // 255))
    return ImageTk.PhotoImage(eye)


def new_page():
    global images
    canvas.delete("all")
    images = [background]
    canvas.create_image(0, 0, image=background, anchor="nw")


def draw_logo(cx, cy, size):
    eye = eye_image(int(size * 0.7))
    images.append(eye)
    gap = int(size * 0.4)
    canvas.create_text(cx - gap, cy, text="C", anchor="e", font=(font_name, -size, "bold"), fill="#D8D8E2")
    canvas.create_image(cx, cy, image=eye)
    canvas.create_text(cx + gap, cy, text="Thru", anchor="w", font=(font_name, -size, "bold"), fill="#D8D8E2")


def pill(cx, cy, w, h, text, size, weight, command=None):
    normal = ImageTk.PhotoImage(rounded(w, h, h // 2, (255, 255, 255, 24), (255, 255, 255, 60), 1))
    bright = ImageTk.PhotoImage(rounded(w, h, h // 2, (255, 255, 255, 60), (255, 255, 255, 130), 1))
    images.append(normal)
    images.append(bright)
    tag = "pill" + str(len(images))
    item = canvas.create_image(cx, cy, image=normal, tags=tag)
    canvas.create_text(cx, cy, text=text, font=(font_name, -size, weight), fill="white", tags=tag)
    if command is not None:
        canvas.tag_bind(tag, "<Enter>", lambda e: canvas.itemconfig(item, image=bright))
        canvas.tag_bind(tag, "<Leave>", lambda e: canvas.itemconfig(item, image=normal))
        canvas.tag_bind(tag, "<Button-1>", lambda e: command())


def show_loading():
    new_page()
    eye = eye_image(58, 90)
    images.append(eye)
    canvas.create_image(W // 2, H // 2, image=eye)
    window.after(1500, show_home)


def show_home():
    stop()
    new_page()
    for x1, y1, x2, y2 in lines:
        canvas.create_line(x1, y1, x2, y2, fill="#8E93B8")
    draw_logo(430, 321, 84)
    for text, cx, cy, w in headings:
        pill(cx, cy, w, 56, text, 24, "bold")
    pill(824, 320, 136, 56, "Credits", 24, "bold", show_credits)
    for text, cx, cy in buttons:
        pill(cx, cy, 134, 54, text, 15, "normal", lambda n=text: show_project(n))


def show_panel(title, message):
    global status
    new_page()
    draw_logo(88, 48, 56)
    panel = ImageTk.PhotoImage(rounded(872, 540, 60, (0, 0, 0, 255), (30, 140, 230, 255), 3))
    images.append(panel)
    canvas.create_image(W // 2, 359, image=panel)
    canvas.create_text(W // 2, 280, text=title, font=(font_name, -40, "bold"), fill="white")
    status = canvas.create_text(W // 2, 335, text=message, anchor="n", font=(font_name, -18), fill="#B9BEDD", justify="center")


def show_project(name):
    if scripts[name].startswith("http"):
        webbrowser.open(scripts[name])
        return
    
    show_panel(name, "")
    pill(434, 48, 150, 56, "Home", 18, "bold", show_home)
    pill(599, 48, 150, 56, "Restart", 18, "bold", lambda: launch(name))
    pill(766, 48, 150, 56, "Stop", 18, "bold", stop)
    launch(name)


def show_credits():
    show_panel("Credits", "\n\n".join(credits))
    pill(766, 48, 150, 56, "Home", 18, "bold", show_home)


def launch(name):
    global running
    stop()
    path = os.path.join(main_folder, scripts[name])
    if not os.path.exists(path):
        canvas.itemconfig(status, text="This file is missing:\n" + scripts[name])
        return
    running = subprocess.Popen([sys.executable, path], cwd=os.path.dirname(path))
    canvas.itemconfig(status, text="Running in its own window.\nPress Stop when you are done.")


def stop():
    global running
    if running is not None:
        if running.poll() is None:
            running.terminate()
        running = None
        canvas.itemconfig(status, text="Stopped. Press Restart to run it again.")


def watch():
    global running
    if running is not None and running.poll() is not None:
        running = None
        canvas.itemconfig(status, text="It closed. Press restart to run it again.\nif it closed by itself, look at the terminal for the error.")
    window.after(500, watch)


def close():
    stop()
    window.destroy()


window = tk.Tk()
window.title("C-Thru")
window.geometry(f"{W}x{H}")
window.resizable(False, False)
window.protocol("WM_DELETE_WINDOW", close)

canvas = tk.Canvas(window, width=W, height=H, highlightthickness=0)
canvas.pack()

for choice in font_choices:
    if choice in tkinter.font.families():
        font_name = choice
        break

background = ImageTk.PhotoImage(next_background())

show_loading()
watch()
animate()
window.mainloop()