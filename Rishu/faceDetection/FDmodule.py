import cv2 as cv
import mediapipe as mp
import time


class FaceDetector():
    def __init__(self, minDetectionCon = 0.75):
        self.minDetectionCon = minDetectionCon
        self.mpFaceDetection = mp.solutions.face_detection
        self.mpDraw = mp.solutions.drawing_utils
        self.faceDetection = self.mpFaceDetection.FaceDetection(min_detection_confidence=self.minDetectionCon)

    def findFaces(self,img,draw = True):
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.faceDetection.process(imgRGB)
        #print(results)
        bboxs = []
        if self.results.detections:
            for id,detection in enumerate(self.results.detections):
                #print(id, detection)
                #print(detection.score)
                #mpDraw.draw_detection(img,detection)
                bboxC = detection.location_data.relative_bounding_box
                imageH, imageW ,imageC = img.shape
                bbox = int(bboxC.xmin * imageW) ,int(bboxC.ymin * imageH),int(bboxC.width * imageW) ,int(bboxC.height * imageH)
                bboxs.append([id,bbox,detection.score])
                if draw:
                    img = self.fDraw(img,bbox)
                    cv.putText(img,f'{int(detection.score[0]*100)}%',(bbox[0],bbox[1] - 20),cv.FONT_HERSHEY_PLAIN,2,(0,255,0),2)
        return img, bboxs
    def fDraw(self,img,bbox,l=30):
        x,y,w,h = bbox
        x1,y1 = x+w,y+h 
        cv.rectangle(img,bbox,(0,255,0),1)
        #topleft x,y
        cv.line(img,(x,y),(x+l,y),(0,255,0),3)
        cv.line(img,(x,y),(x,y+l),(0,255,0),3)
        #topright x,y
        cv.line(img,(x1,y),(x1-l,y),(0,255,0),3)
        cv.line(img,(x1,y),(x1,y+l),(0,255,0),3)
        #bottomleft x,y1
        cv.line(img,(x,y1),(x+l,y1),(0,255,0),3)
        cv.line(img,(x,y1),(x,y1-l),(0,255,0),3)
        #bottomright x1,y1
        cv.line(img,(x1,y1),(x1-l,y1),(0,255,0),3)
        cv.line(img,(x1,y1),(x1,y1-l),(0,255,0),3)
        return img



def main():
    cap = cv.VideoCapture(0)
    pTime = 0    
    detector = FaceDetector()
    
    while True:
        success, img = cap.read()
        img,bboxs = detector.findFaces(img)
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv.putText(img,f'FPS: {int(fps)}',(20,60),cv.FONT_HERSHEY_PLAIN,3,(105, 105, 105),2)
        cv.imshow("Image",img)
        cv.waitKey(1)
    
if __name__ == "__main__":
    main()