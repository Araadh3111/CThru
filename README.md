# C-Thru : A Collaborative OpenCV Project with multiple modes.

## About

C-Thru is a collaborative project made by us (Araadh,Siddak,Rishu).
It features multiple OpenCV Project grouped into a single app for anyone to try it out or alter with it.

---
# How to Use the App (very important):
1) open terminal after cloning the repo in ure desktop or downloading it.
2) make sure u are in the cthru folder, if not go there by writing 'cd Cthru' in the terminal.
3) after that type py -3.11 py -3.11 desktop/cthru.py.
4) once that step is done an interface like this should open.
<img width="1127" height="837" alt="image" src="https://github.com/user-attachments/assets/ea04b4ac-9017-47ed-88ee-ddae0251e5e2" />
5) Select a Button from the availaible options to see the program work.
6) Please see the ASL part (developed by me (Araadh)) will take u to the website 'https://cthru.vercel.app/' and to use the ASL feature please refer to the hand signs attatched below.

## Images of different programs

### ASL:
<img width="1917" height="982" alt="image" src="https://github.com/user-attachments/assets/598b5e90-6e1e-4b7d-bef9-e539b872af8f" />

### Hand Detector:
<img width="925" height="730" alt="image" src="https://github.com/user-attachments/assets/5911eea2-49a5-40c7-9b28-db222009ac22" />

### Face Mesh:
<img width="797" height="685" alt="image" src="https://github.com/user-attachments/assets/6777e5fe-7861-4c02-9d25-21fb13c44b13" />

### Face Box:
<img width="670" height="633" alt="image" src="https://github.com/user-attachments/assets/d8c7db35-f10d-4733-b348-183f29a6e94a" />

### Pose Detector:
<img width="447" height="630" alt="image" src="https://github.com/user-attachments/assets/d604c2f4-b882-4940-9d62-9726ec7a4162" />

### Face Blur:
<img width="536" height="682" alt="image" src="https://github.com/user-attachments/assets/958d444a-8ef6-4a92-8e18-16d02c2c50cb" />

### Virtual Painter:
<img width="1220" height="936" alt="image" src="https://github.com/user-attachments/assets/7467a741-97d8-45a4-ae96-5ae49ae33d3d" />

### Finger Count
<img width="745" height="630" alt="image" src="https://github.com/user-attachments/assets/8fbaa1bf-5099-45bb-8ccd-916c392a8a70" />


---
## Sections

### Araadh

Sign language recognition

### Siddak

1.Shape Detection

2.Virtual Painter

3.Gesture Volume Control(only for mac)

### Rishu

1.Pose Estimation(module)

2.Hand Tracking(module)

3.Color Displayer

4.Face Tracker

---
## Tech Stack
### Python and Libraries:-
- OpenCV (Python)
- MediaPipe
- scikit-learn
- Fast API
- Tkinter
- Numpy
- Pyttsx3
- os
- subprocess
- sys
- pickle
- pandas
- math
- 

---
# Project Details:-

## Sign Language Recognition (ASL)
Sign Language Recognition is a machine learning pipeling which uses some custom dataset(custom collected samples) and mostly the letters are from a dataset from Kaggle (https://www.kaggle.com/datasets/grassknoted/asl-alphabet?resource=download) which has positions of hand in American Sign
Language(ASL) letters in varying angles and positions and lightings for the machine to learn better.

The file (recognize_words.py) collects webcam data normalizes the data relative to the wrist position and then the model predicts what the letter could be and presents it as text.

### How it works
Webcam → MediaPipe in the browser → 21 hand points (63 numbers) → FastAPI server → Random Forest model → letter → text

### Libraries used :-
- OpenCV
- Numpy
- pyttsx3
- pickle
- mediapipe
### Project Structure :-
```
CThru/
├── .../
├── Araadh/
│   ├── recognize_words.py 
└── README.md
```

### Dataset Samples

### A
<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/64d6594d-5633-4348-8517-93f29796b04f" />


### B
<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/eb717e46-7b7d-44bd-bfa2-54b28ffe5183" />


### C
<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/244d98db-ce8f-4eac-a232-d0e25bb44ee2" />


### D
<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/bc97ab94-4cfb-4a67-a375-5d95a8f297f0" />

### E
<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/e18c9fd6-da3d-4b61-86df-dac5825aff2f" />

### F
<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/bbdd3852-67a0-4c04-91f0-32c67cf40643" />


### G
<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/d08b9ef0-517b-482f-9c10-05d1e84f805f" />


### H
<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/428a8cbb-9a59-4209-ab97-f8e2e926f3c3" />

### I
<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/6d6b3c93-a4c9-4921-8b8b-e6c4cfe84851" />

### J
<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/139975a4-7c9b-4995-b93b-8c1c5242ca4d" />

### K
<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/e6fd2b2f-3a82-4d93-8b46-c0deecac5aba" />

### L
<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/1efea42d-8768-4fb7-8b7d-b4dbd7b3a1f6" />

### M
<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/269f89ff-5f8e-4c79-80e5-37a68caa5e4a" />

### N
<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/7ed7fd9f-c36a-44a2-a2d0-a9facce5be1a" />

### O
<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/0f8384f3-6ad7-4d1c-bae1-c3771dda34fd" />

### P
<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/34d5a3d5-6042-49f2-9d3c-ef7d6a6d7194" />

### Q
<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/64505ef8-bd34-44e9-b650-63a18334926f" />

### R
<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/ca3ff729-fa0c-426c-9d4b-167c7716b052" />

### S
<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/86605be2-9c56-4c24-8ed3-a9a9d79e15f9" />

### T
<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/0ad35d2d-5a9f-4175-b2bf-35d6f66dd954" />

### U
<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/31c40b09-4a42-4b93-ae02-5909d75f33b7" />

### V
<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/d436baf4-c5e9-4300-9222-cfb4ce6f17c5" />

### W
<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/fa15b7dc-7e0b-410b-8402-beda91514272" />

### X
<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/9412bcfe-2b5e-45c5-b47c-bd09aa11de21" />

### Y
<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/634bf30a-8349-4827-9aaa-476a99a09cce" />


### Z
<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/cf6f8bd4-32c8-41fa-a6a2-29cb333aa290" />

### SPACE: 
<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/b13da0e6-f7c1-4c68-9967-5b956fe85b4e" />



## Features of C Thru Sign detection:
- Recognizes 29 signs: A to Z, space, backspace and clear
- Live hand skeleton drawn over the camera
- Shows the current sign and its confidence
- Hold a sign steady to type the letter, so shaky hands do not add random letters
- Suggests up to three words as you spell
- Pick a suggestion by clicking it, or by pointing at it for one second
- Speak button reads the text out loud
- Runs in the browser, nothing to install: https://cthru.vercel.app/



### Please Note:
The Sign for Clearing all the text is 👍 thumbs up and The Sign for Using backspace is 👎 thumbs down.

### AI usage declaration:
I have used Claude to fix the vercel deployment error by helping me make **some** changes in the script .js file.


---

## Shape Detection
A shape detector that tracks the user's hand and correctly guesses(almost) the shape they make using their hands!


### Libraries used :-
- OpenCV
- Numpy
### Project Structure :-
```
CThru/
├── .../
├── siddakjr/
│   ├── shape_detection.py 
└── README.md
```
---

## Virtual Painter
A virtual painter that lets you draw on your screen using your hands!
Raise a single finger to draw and raise two fingers to select between the color/highlighter/eraser(by still raising both the fingers and pointing them on top of the option basically moving your finger on the option you want to select) and then raise a single finger again to draw/ erase using whatever option you selected.

### Libraries used :-
- OpenCV
- Numpy
- OS
- time
### Project Structure :-
```
CThru/
├── .../
├── siddakjr/
│   ├── VirtualPainter.py 
└── README.md
```
---

## Gesture Volume Control(WORKS ONLY ON MACBOOK)
Control your device's volume using your fingers!

### Libraries used :-
- OpenCV
- Numpy
- OS
- time
### Project Structure :-
```
CThru/
├── .../
├── siddakjr/
│   ├── VolumeHandControl.py
└── README.md
```
---
## Pose Estimation
A module that tracks the user's body, it is built using mediapipe and has 33 unique points that maps the user's whole body. It change be used to monitor body position for different purposes and serves the purpose of a module to build projects on (coming in next ship!).

### Libraries used :-
- MediaPipe
- OpenCV
- Time (for framerates)
### Project Structure :-
```
CThru/
├── .../
├── Rishu/
│   ├── poseEstimation/
│   │   ├── PEmodule.py 
│   │   └── poseEstimation.py
└── README.md
```
---
## Hand Tracking
A module that tracks the user's and, it is built using mediapipe and has 21 unique points that maps the user's hands (can be more than one user too). It change be used for gesture controls and accessibility etc and serves the purpose of a module to build projects on.


### Libraries used :-
- MediaPipe
- OpenCV
- Time (for framerates)
### Project Structure :-
```
CThru/
├── .../
├── Rishu/
│   ├── handTracking/
│   │   ├── HTmodule.py 
│   │   └── handTracking.py
└── README.md
```
---
## Color Displayer
It can be used to display certain colours from a web cam, image or video. (currently set to blue, a customizable selector will be add when the dashboard is done.)

### Libraries used :-
- OpenCV
- Numpy
### Project Structure :-
```
CThru/
├── .../
├── Rishu/
│   ├── color_displayer.py
└── README.md
```
---
## Face Tracker (basic)
A basic face tracker built on opencv (better version and a mesh version will be added in next ship!)


### Libraries used :-
- OpenCV
- Numpy
### Project Structure :-
```
CThru/
├── .../
├── Rishu/
│   ├── facial_tracker.py 
└── README.md
```
---
