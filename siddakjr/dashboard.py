import tkinter as tk
from PIL import Image, ImageTk, ImageFilter, ImageDraw, ImageEnhance
import subprocess
import sys
import os

folder = os.path.dirname(os.path.abspath(__file__))
W, H = 1000, 640

if sys.platform == "win32":
    font_name = "Segoe UI"
else:
    font_name = "Helvetica Neue"

models = {
    "Shape Detector": "shape_detection.py",
    "Volume Control": "VolumeHandControl.py",
    "Screen Designer": "VirtualPainter.py",
    "Sign Language": "sign_language.py",
    "Face and Eye Mask": "face_mask.py",
}

running = None
images = []  # tkinter deletes images if you dont keep them somewhere

bg = Image.open(os.path.join(folder, "bg.jpg")).convert("RGB").resize((W, H))
blurred = bg.filter(ImageFilter.GaussianBlur(25))


def glass_card(x, y, w, h, hover=False):
    # cut out the blurred part of the background behind the card
    piece = blurred.crop((x, y, x + w, y + h))

    if hover:
        piece = ImageEnhance.Brightness(piece).enhance(1.35)
        piece = Image.blend(piece, Image.new("RGB", (w, h), "white"), 0.15)
    else:
        piece = ImageEnhance.Brightness(piece).enhance(1.2)
        piece = Image.blend(piece, Image.new("RGB", (w, h), "white"), 0.08)

    draw = ImageDraw.Draw(piece)
    draw.rounded_rectangle((0, 0, w - 1, h - 1), radius=28, outline="white", width=2)

    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, w - 1, h - 1), radius=28, fill=255)
    piece.putalpha(mask)

    return ImageTk.PhotoImage(piece)


def make_card(x, y, w, h, text, size, on_click):
    normal = glass_card(x, y, w, h)
    hover = glass_card(x, y, w, h, hover=True)
    images.append(normal)
    images.append(hover)

    tag = "card" + str(len(images))
    img = canvas.create_image(x, y, image=normal, anchor="nw", tags=tag)

    canvas.create_text(x + w // 2 + 1, y + h // 2 + 1, text=text,
                       font=(font_name, size, "bold"), fill="#333333", tags=tag)
    canvas.create_text(x + w // 2, y + h // 2, text=text,
                       font=(font_name, size, "bold"), fill="white", tags=tag)

    canvas.tag_bind(tag, "<Enter>", lambda e: canvas.itemconfig(img, image=hover))
    canvas.tag_bind(tag, "<Leave>", lambda e: canvas.itemconfig(img, image=normal))
    canvas.tag_bind(tag, "<Button-1>", lambda e: on_click())


def launch(name):
    global running
    path = os.path.join(folder, models[name])

    if not os.path.exists(path):
        canvas.itemconfig(status, text=name + " is not ready yet")
        return

    if running is not None and running.poll() is None:
        running.terminate()

    running = subprocess.Popen([sys.executable, path], cwd=folder)
    canvas.itemconfig(status, text="Running: " + name)


def stop():
    if running is not None and running.poll() is None:
        running.terminate()
        canvas.itemconfig(status, text="Stopped")
    else:
        canvas.itemconfig(status, text="Nothing is running")


def close():
    if running is not None and running.poll() is None:
        running.terminate()
    window.destroy()


window = tk.Tk()
window.title("C-Thru")
window.geometry(f"{W}x{H}")
window.resizable(False, False)
window.protocol("WM_DELETE_WINDOW", close)

canvas = tk.Canvas(window, width=W, height=H, highlightthickness=0)
canvas.pack()

bg_photo = ImageTk.PhotoImage(bg)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

canvas.create_text(W // 2 + 2, 92, text="C-THRU", font=(font_name, 56, "bold"), fill="#333333")
canvas.create_text(W // 2, 90, text="C-THRU", font=(font_name, 56, "bold"), fill="white")

positions = [(80, 190), (370, 190), (660, 190), (225, 370), (515, 370)]
for name, (x, y) in zip(models, positions):
    make_card(x, y, 260, 150, name, 20, lambda n=name: launch(n))

make_card(420, 545, 160, 50, "STOP", 16, stop)

status = canvas.create_text(W // 2, 618, text="", font=(font_name, 13), fill="white")

window.mainloop()