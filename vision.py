import cv2
import numpy as np

class cvImgAnalysis:

    def __init__(self, cam, lowerThresh, upperThresh):
        self.cap = cv2.VideoCapture(cam)
        assert self.cap.isOpened(), 'No cam'
        self.lowerThresh = lowerThresh
        self.upperThresh = upperThresh

    def getCoords(self, printVals=False):
        while True:
            img = self.getMaskedImg(printVals)
            cont = self.getContours(img, printVals=printVals)
            if cont.shape[0] == 4:
                break
        if printVals:
            self.drawContours(img, [cont])
        return self.sortCoords(cont, printVals=printVals)

    def sortCoords(self, cont, clockWise=False, printVals=False):
        coords = np.reshape(cont, (4, 2)).tolist()
        print(coords)
        coords.sort(self.coordsCompare)
        if clockWise:
            coords = [coords[1], coords[3], coords[2], coords[0]]
        if printVals:
            print(coords)
        return coords

    def coordsCompare(self, point1, point2):
        return point1[1] - point2[1] if point1[1] - point2[1] else point1[0] - point2[0]

    def drawContours(self, img, contours, index=-1, color=(255, 0, 0), thickness=3):
        cv2.drawContours(img, contours, index, color, thickness)
        cv2.imwrite('contImg.png', img)

    def getContours(self, img, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE, maxCont=True, printVals=False):
        contours, hierarchy = cv2.findContours(img.copy(), mode, method)
        if maxCont:
            if len(contours):
                cont = max(contours, key=cv2.contourArea)
                return cv2.approxPolyDP(cont, 0.05*cv2.arcLength(cont,True), True)
            else:
                return np.zeros((1, 1, 2), dtype=np.uint8)
        return contours

    def getMaskedImg(self, printVals=False):
        frame = self.readFrame(printVals)
        mask = self.getMask(frame)
        gray = self.getGray(frame)
        img = cv2.bitwise_and(gray, gray, mask=mask)
        if printVals:
            cv2.imwrite('img.png', img)
        return img

    def readFrame(self, printVals=False):
        flag, frame = self.cap.read()
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

if __name__ == '__main__':
    cam = cvImgAnalysis(0, lowerThresh=np.uint8([140, 70, 90]), upperThresh=np.uint8([180, 255, 255]))
    cam.getCoords(True)

    cam.release()
