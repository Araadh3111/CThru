#Pose Estimation Module

import cv2 as cv
import mediapipe as mp
import time

class poseDetector():

    def __init__(self,mode=False,modelComplexity = 1, smooth = True,enableSeg=False, smoothSeg=True, detectionCon = 0.5, trackCon = 0.5):
        
        self.mode = mode
        self.modelComplexity = modelComplexity
        self.smooth = smooth
        self.enableSeg = enableSeg
        self.smoothSeg = smoothSeg
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode,self.modelComplexity,self.smooth,self.enableSeg,self.smoothSeg,self.detectionCon,self.trackCon)

    def findPose(self,img,draw=True):
        imgRGB = cv.cvtColor(img,cv.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
    #print(results.pose_landmarks)
        if self.results.pose_landmarks:
            if draw:
                 self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,self.mpPose.POSE_CONNECTIONS)
        return img

    def findPosition(self,img, draw=True):
        lmList=[]
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h,w,c = img.shape
                #print(id,lm)
                cx, cy = int(lm.x*w),int(lm.y*h)
                lmList.append([id,cx,cy])
                if draw:
                    cv.circle(img,(cx,cy),5,(255,0,0),-1)

        return lmList


def main():
    mpPose = mp.solutions.pose
    pose = mpPose.Pose()
    mpDraw = mp.solutions.drawing_utils

    cap = cv.VideoCapture(0)
    ptime = 0
    detector = poseDetector()

    while True:
        success, img = cap.read()
        img = detector.findPose(img)
        lmList = detector.findPosition(img,draw =False)
        if len(lmList) != 0:
            print(lmList[8])
            #cv.circle(img,(lmList[8][1],lmList[8][2]),5,(255,0,0),-1)
        ctime = time.time() 
        fps = 1/(ctime-ptime)
        ptime = ctime
        cv.putText(img, str(int(fps)),(70,50), cv.FONT_HERSHEY_COMPLEX,3 ,(255,0,0),3 )
        cv.imshow("Pose", img)
        cv.waitKey(1)

if __name__ == "__main__":
    main()
    