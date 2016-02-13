#!/usr/bin/python

import time
import base64

import numpy
import cv2

import netTable
import stabilizer
from vision import cvImgAnalysis
from stabilizer import Stabilizer


GOAL_WIDTH = 20.0
GOAL_HEIGHT = 14.0

class VisionPoster:

    def __init__(self, width, height, focalLength):
        self.networkTable = netTable.makeNetworkTable('roborio-1619-frc.local', 'SmashBoard')
        self.camera = cvImgAnalysis(0, numpy.uint8([35, 100, 35]), numpy.uint8([120, 255, 255]), width, height, focalLength, GOAL_WIDTH, GOAL_HEIGHT)
        self.distanceStabilizer = Stabilizer(10, 10)
        self.pivotalAngleStabilizer = Stabilizer(10, 7.5)
        self.centerXStabilizer = Stabilizer(10, 5)
        self.distanceToOptimalStabilizer = Stabilizer(10, 7.5)
        self.angleToOptimalStabilizer = Stabilizer(10, 10)

    def getFrame(self):
        frame = self.camera.readFrame()
        flag, coordinates, centerX = self.camera.getCoords(False, False, frame)
        if flag:
            try:
                certified, distance, pivotalAngle, distanceToOptimal, angleToOptimal, errors = self.camera.getVertexData(coordinates)
                if self.distanceStabilizer.push(distance):
                    self.networkTable.putNumber('distance', self.distanceStabilizer.get())
                if self.pivotalAngleStabilizer.push(pivotalAngle):
                    self.networkTable.putNumber('pivotalAngle', self.pivotalAngleStabilizer.get())
                if self.centerXStabilizer.push(centerX):
                    self.networkTable.putNumber('centerX', self.centerXStabilizer.get())
                if self.distanceToOptimalStabilizer.push(distanceToOptimal):
                    self.networkTable.putNumber('distanceToOptimal', self.distanceToOptimalStabilizer.get())
                if self.angleToOptimalStabilizer.push(angleToOptimal):
                    self.networkTable.putNumber('angleToOptimal', self.angleToOptimalStabilizer.get())
            except ZeroDivisionError:
                print('Divide by zero error')
        self.networkTable.putString('image', self.getSmashBoardImage(flag, coordinates, frame))

    def getSmashBoardImage(self, flag, coordinates, frame):
        if flag:
            self.camera.drawContours(frame, [numpy.array(coordinates).reshape((-1, 1, 2))], displayCam=False)
        frame = cv2.resize(frame, (0, 0), fx=0.234375, fy=0.234375)
        image = cv2.imencode('.jpg', frame)[1]
        return base64.b64encode(image)

    def cleanUp(self):
        self.camera.release()


if __name__ == '__main__':
    poster = VisionPoster(640, 480, 732)
    while True:
        poster.getFrame()
    poster.cleanUp()
