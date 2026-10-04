import cv2 as cv
import mediapipe as mp
import time

cap = cv.VideoCapture(0)

while True:
    succes, img = cap.read()