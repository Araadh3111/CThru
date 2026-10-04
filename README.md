# C-Thru : A Collaborative OpenCV Project with multiple modes.

## About

C-Thru is a collaborative project made by us (Araadh,Siddak,Rishu).
It features multiple OpenCV Project grouped into a single app for anyone to try it out or alter with it.

---
## Sections
### Araadh
Sign language recognition

### Siddak
1.Shape Detection
2.Virtual Painter
3.Gesture Volume Control

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

---
# Project Details:-

## Pose Estimation
A module that tracks the user's body, it is built using mediapipe and has 33 unique points that maps the user's whole body. It change be used to monitor body position for different purposes and serves the purpose of a module to build projects on (coming in next ship!).
### How to use :-

1.Clone the repo (https://github.com/Araadh3111/CThru.git).
2.Navigate to /Rishu/poseEstimation/PEmodule.py 
3.Download the required libraries (pip install {library name} )
4.Run the project.

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
### How to use :-

1.Clone the repo (https://github.com/Araadh3111/CThru.git).
2.Navigate to /Rishu/handTracking/HTmodule.py 
3.Download the required libraries (pip install {library name} )
4.Run the project.

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
### How to use :-

1.Clone the repo (https://github.com/Araadh3111/CThru.git).
2.Navigate to /Rishu/color_displayer.py 
3.Download the required libraries (pip install {library name} )
4.Run the project.

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
### How to use :-
1.Clone the repo (https://github.com/Araadh3111/CThru.git).
2.Navigate to /Rishu/facial_tracker.py  
3.Download the required libraries (pip install {library name} )
4.Run the project.

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
(the read me file is not finished it will be finished asap (im making this at 1 am what do you expect dawg.))
