import tkinter as tk
import subprocess
import sys 
import os 

folder = os.path.dirname(os.path.abspath(__file__))

bg_color = "#111111"
card_color = "#1c1c1c"
hover_color = "#2a2a2a"
accent = "#ff4655"

models = {
    "Shape Detector": "shape_detection.py",
    "Volume Control": "VolumeHandControl.py",
    "Screen Designer": "VirtualPainter.py",
    "Sign Language": "sign_language.py",
    "Face and Eye Mask": "face_mask.py"
}

running = None

def launch(name):
    global running
    path = os.path.join(folder, models[name])

    if not os.path.exists(path):
        status.config(text=name + " is not ready yet")
        return

    if running is not None and running.poll() is None:
        running.terminate()

    running = subprocess.Popen([sys.executable, path], cwd=folder)
    status.config(text="Running: " + name)

def stop():
    global running 
    if running is not None and running.poll() is None:
        running.terminate()
        status.config(text="Stopped")
    else:
        status.config(text="Nothing is running")

def on_enter(e):
    e.widget.config(bg=hover_color)

def on_leave(e):
    e.widget.config(bg=card_color)

def close():
    if running is not None and running.poll() is None:
        running.terminate()
    window.destroy()

window = tk.Tk()
window.title("C-Thru")
window.geometry("900x620")
window.config(bg = bg_color)
window.protocol("WM_DELETE_WINDOW", close)

title = tk.Label(window, text = "C-THRU", font=("Futura", 48, "bold"), fg=accent, bg=bg_color)
title.pack(pady=(40, 0))

subtitle = tk.Label(window, text="pick a model to start", font=("Futura", 14), fg="gray", bg=bg_color)
subtitle.pack(pady=(0,30))

grid = tk.Frame(window, bg=bg_color)
grid.pack()


row = 0
col = 0
for name in models:
    card = tk.Label(grid, text=name, font=("Futura", 18), fg="white", bg=card_color,
                    width=18, height=4, cursor="hand2")
    card.grid(row=row, column=col, padx=10, pady=10)
    card.bind("<Button-1>", lambda e, n=name: launch(n))
    card.bind("<Enter>", on_enter)
    card.bind("<Leave>", on_leave)

    col += 1
    if col == 3:
        col = 0
        row += 1

stop_btn = tk.Label(window, text="STOP", font=("Futura", 16, "bold"), fg="white", bg=accent,
                    width=12, height=2, cursor="hand2")

stop_btn.pack(pady=30)
stop_btn.bind("<Button-1>", lambda e: stop())

status = tk.Label(window, text="", font=("Futura", 12), fg="gray", bg=bg_color)
status.pack()

window.mainloop()
    