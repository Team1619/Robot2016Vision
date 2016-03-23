
import socket
import time

import cv2
import numpy

class ImageStreamer:

    def __init__(self, host='10.16.19.50', port=1619):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host = host
        self.port = port

    # takes plain image byte data
    def sendImage(self, imageData):
        self.socket.sendto(imageData + '\n', (self.host, self.port))

if __name__ == '__main__':
    streamer = ImageStreamer()
    cap = cv2.VideoCapture(0)
    assert cap.isOpened(), 'no cap'
    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        data = numpy.array(cv2.imencode('.jpg', frame)[1])
        streamer.sendImage(data.tostring())
