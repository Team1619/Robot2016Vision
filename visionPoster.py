#!/usr/bin/python

import time
import base64

import numpy
import scipy
import cv2

import netTable
from smashBoard import SmashBoard
from imageStreamer import ImageStreamer

from vision import cvImgAnalysis
from stabilizer import Stabilizer


GOAL_WIDTH = 20.0
GOAL_HEIGHT = 12.0
CONTRAST_SCALE = 1.0
BRIGHTNESS_INCREASE = 0
MIN_CONTOUR_AREA = 100

class VisionPoster:

    def __init__(self, width, height, focalLength):
        self.socketTable = SmashBoard(host='10.16.19.2')
	self.socketTable.connect()
	self.socketTable.startUpdateThread()
        self.imageStreamer = ImageStreamer()
	#self.networkTable = netTable.makeNetworkTable('roborio-1619-frc.local', 'SmashBoard')
        self.camera = cvImgAnalysis(0, numpy.uint8([56, 100, 25]), numpy.uint8([112, 255, 255]), width, height, focalLength, GOAL_WIDTH, GOAL_HEIGHT, MIN_CONTOUR_AREA)
        self.distanceStabilizer = Stabilizer(20, 10)
        #self.pivotalAngleStabilizer = Stabilizer(10, 7.5)
        self.centerXStabilizer = Stabilizer(4, 5)
        #self.centerYStabilizer = Stabilizer(4, 5)
        #self.distanceToOptimalStabilizer = Stabilizer(10, 7.5)
        #self.angleToOptimalStabilizer = Stabilizer(10, 10)
        self.angleOffsetToAlignedStabilizer = Stabilizer(2, 5)
        #self.verticalAngleStabilizer = Stabilizer(10, 5)

    def getFrame(self):
        frame = self.camera.readFrame()
        #frame = numpy.array(frame[::-1, ::-1, :])
        flag, coordinates, centerX, _ = self.camera.getCoords(False, False, frame)
        if flag:
            try:
                _, distance, _, angleOffsetToAligned, _, _, _, _ = self.camera.getVertexData(coordinates)
                if self.distanceStabilizer.push(distance):
                    self.socketTable.setDouble('distance', self.distanceStabilizer.get())
                #if self.pivotalAngleStabilizer.push(pivotalAngle):
                #    self.networkTable.putNumber('pivotalAngle', self.pivotalAngleStabilizer.get())
                if self.centerXStabilizer.push(centerX):
                    self.socketTable.setLong('centerX', self.centerXStabilizer.get())
                #    self.networkTable.putNumber('angleOffsetToAlignedCG', self.camera.getAngleOffsetToAlignedCG(centerX))
                #if self.centerYStabilizer.push(centerY):
                #    self.networkTable.putNumber('centerY', self.centerYStabilizer.get())
                if self.angleOffsetToAlignedStabilizer.push(angleOffsetToAligned):
                    adjustedAngleOffset = self.angleOffsetToAlignedStabilizer.get() - 3
                    if adjustedAngleOffset < 0:
                        adjustedAngleOffset += (0.7/25) * adjustedAngleOffset
                    else:
                        adjustedAngleOffset += (0.7/13) * adjustedAngleOffset
                    #print adjustedAngleOffset
                    self.socketTable.setDouble('angleOffsetToAligned', adjustedAngleOffset)
                #if self.verticalAngleStabilizer.push(verticalAngle):
                #    self.networkTable.putNumber('verticalAngle', self.verticalAngleStabilizer.get())
                #if self.distanceToOptimalStabilizer.push(distanceToOptimal):
                #    self.networkTable.putNumber('distanceToOptimal', self.distanceToOptimalStabilizer.get())
                #if self.angleToOptimalStabilizer.push(angleToOptimal):
                #    self.networkTable.putNumber('angleToOptimal', self.angleToOptimalStabilizer.get())
            except ZeroDivisionError:
                print('Divide by zero error')
        self.socketTable.setLong('contourFound', int(flag))
        #self.socketTable.setString('image', self.getSmashBoardImage(flag, coordinates, frame))
        self.imageStreamer.sendImage(self.getSmashBoardImage(flag, coordinates, frame))

    def getSmashBoardImage(self, flag, coordinates, frame):
        if flag:
            self.camera.drawContours(frame, [numpy.array(coordinates).reshape((-1, 1, 2))], displayCam=False)
        frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        #frame = cv2.multiply(frame, numpy.array([CONTRAST_SCALE]))
        #frame = cv2.add(frame, BRIGHTNESS_INCREASE)
        image = numpy.array(cv2.imencode('.jpg', frame)[1])
        return image.tostring()

    def cleanUp(self):
        self.camera.release()


if __name__ == '__main__':
    #time.sleep(10)
    poster = VisionPoster(640, 480, 732)
    while True:
        poster.getFrame()
    poster.cleanUp()
