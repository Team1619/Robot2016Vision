import cv2
import numpy as np
from coordinateCalculator import vertexMath
import subprocess
import time

class cvImgAnalysis:
    CAMERA_COMMAND = 'v4l2-ctl -c exposure_auto=1 -c exposure_absolute=5 -c backlight_compensation=0 -c sharpness=50 -c brightness=30 -c contrast=5'

    def __init__(self, cam, lowerThresh, upperThresh, imgWidth, imgHeight, focal, realWidth, realHeight, minContourArea):
        self.cap = cv2.VideoCapture(cam)
        assert self.cap.isOpened(), 'No cam'
        #while not self.cap.isOpened():
        #    print('No cam, but wait')
        #    time.sleep(1)
        #    self.cap = cv2.VideoCapture(cam)
        self.lowerThresh = lowerThresh
        self.upperThresh = upperThresh
        self.minArea = minContourArea
        #subprocess.check_call(self.CAMERA_COMMAND.split(), shell=False)
        self.targetTrig = vertexMath(imgWidth, imgHeight, focal, realWidth, realHeight, armSideOffset=12)

    def getVertexData(self, coords):
        return self.targetTrig.getVertexData(coords)

    def getCoords(self, printVals=False, displayCam=False, frame=None):
        img = self.getMaskedImg(printVals, frame=frame)
        cont = self.getContours(img, printVals=printVals)
        if printVals:
            self.drawContours(img, [cont], displayCam=False)
        elif displayCam:
            self.drawContours(img, [cont], displayCam=True)
        if self.checkContour(cont):
            return (True, self.sortCoords(cont, True, printVals=printVals), self.getCenterX(cont), self.getCenterY(cont))
        return False, [0], -1, -1

    def sortCoords(self, cont, clockWise=False, printVals=False):
        coords = np.reshape(cont, (4, 2)).tolist()
        if printVals:
            print(coords)
        if clockWise:
            coords = [coords[3], coords[2], coords[1], coords[0]]
        if printVals:
            print(coords)
        return coords

    def checkContour(self, cont):
        return cont.shape[0] == 4 and cv2.contourArea(cont) > self.minArea

    def coordsCompare(self, point1, point2):
        return point1[1] - point2[1] if point1[1] - point2[1] else point1[0] - point2[0]

    def drawContours(self, img, contours, index=-1, color=(255, 0, 0), thickness=3, displayCam=False, writeImg=False):
        cv2.drawContours(img, contours, index, color, thickness)
        if displayCam:
            cv2.imshow('img', img)
            # cv2.waitKey must be called if displayCam is True
        elif writeImg:
            cv2.imwrite('contImg.png', img)

    def getCenterX(self, cont):
        moment = cv2.moments(cont)
        return int(moment['m10']/moment['m00'])

    def getCenterY(self, cont):
        moment = cv2.moments(cont)
        return int(moment['m01']/moment['m00'])

    def getAngleOffsetToAlignedCG(self, centerX):
        return self.targetTrig.getAngleToCentralX(centerX)

    def getContours(self, img, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE, maxCont=True, printVals=False):
        contours, hierarchy = cv2.findContours(img.copy(), mode, method)
        if maxCont:
            if len(contours):
                cont = max(contours, key=cv2.contourArea)
                hull = cv2.convexHull(cont)
                return cv2.approxPolyDP(hull, 0.05*cv2.arcLength(hull,True), True)
            else:
                return np.zeros((1, 1, 2), dtype=np.uint8)
        return contours

    def getMaskedImg(self, printVals=False, frame=None):
        if frame is None:
            frame = self.readFrame(printVals)
        mask = self.getMask(frame)
        gray = self.getGray(frame)
        img = cv2.bitwise_and(gray, gray, mask=mask)
        if printVals:
            cv2.imwrite('img.png', img)
        return img

    def readFrame(self, printVals=False):
        flag, frame = self.cap.read()
        #while not flag:
        #    flag, frame = self.cap.read()
        assert flag, 'No frame'
        if printVals:
            print(frame.shape)
        frame = cv2.GaussianBlur(frame, (5, 5), 0)
        return frame

    def getMask(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lowerThresh, self.upperThresh)
        return mask

    def getGray(self, frame):
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    cam = cvImgAnalysis(0, lowerThresh=np.uint8([0, 0, 40]), upperThresh=np.uint8([180, 255, 255]))

    while True:
        coords = cam.getCoords(False, True)
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
        print(coords)
        targetTrig = vertexMath(640, 480, 732, 20.0, 14.0)
        targetTrig.getVertexData(coords)
    cam.release()
