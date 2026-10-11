import cv2 as cv
import mediapipe as mp
import time

class FaceMeshDetector():
    def __init__(self,staticMode = False, maxFaces = 2,minDetectionCon = 0.5,minTrackCon = 0.5):
        self.staticMode = staticMode
        self.maxFaces = maxFaces
        self.minDetectionCon = minDetectionCon
        self.minTrackCon = minTrackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpFaceMesh = mp.solutions.face_mesh
        self.faceMesh = self.mpFaceMesh.FaceMesh(static_image_mode = self.staticMode , max_num_faces = self.maxFaces, min_detection_confidence = self.minDetectionCon, min_tracking_confidence = self.minTrackCon)
        self.drawSpec = self.mpDraw.DrawingSpec(color=(0,255,0),thickness=1,circle_radius=1)

    def findFaceMesh(self,img,draw = True):
        self.imgRGB = cv.cvtColor(img,cv.COLOR_BGR2RGB)
        self.results = self.faceMesh.process(self.imgRGB)
        faces =[]
        if self.results.multi_face_landmarks:
            for faceLms in self.results.multi_face_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, faceLms,self.mpFaceMesh.FACEMESH_TESSELATION,self.drawSpec,self.drawSpec)
                face = []
                for id,lm in enumerate(faceLms.landmark):
                    ih,iw,ic = img.shape
                    x,y = int(lm.x*iw), int(lm.y*ih)
                    #print(id,x,y)
                    #(detect points)cv.putText(img,str(id),(x,y),cv.FONT_HERSHEY_PLAIN,0.2,(105, 105, 105),1)
                    face.append([x,y])
                faces.append(face)
                
        return img ,faces


def main():
    cap = cv.VideoCapture(0)
    pTime = 0
    detector = FaceMeshDetector()
    while True:
        success, img = cap.read()
        img,faces = detector.findFaceMesh(img)
        if len(faces) != 0:
            print (len(faces))
            #print(faces[0])
            #print(len(faces[0]))
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv.putText(img,f'FPS: {int(fps)}',(20,60),cv.FONT_HERSHEY_PLAIN,3,(105, 105, 105),2)
        cv.imshow("Image",img)
        cv.waitKey(1)

if __name__ =="__main__":
    main()