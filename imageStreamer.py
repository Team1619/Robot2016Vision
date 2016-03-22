
import socket
import time

import cv2
import numpy

class ImageStreamer:

    def __init__(self, host='192.168.1.126', port=1619):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host = host
        self.port = port

    # takes plain image byte data
    def sendImage(self, imageData):
        self.socket.sendto(imageData, (self.host, self.port))

if __name__ == '__main__':
    streamer = ImageStreamer()
    cap = cv2.VideoCapture(0)
    assert cap.isOpened(), 'no cap'

    # lol = cv2.imdecode(numpy.fromstring(byteArray, dtype='uint8'), 1)
    # cv2.imshow('SERVER',lol)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    while True:
        ret, frame = cap.read()
        assert ret, 'no frame'
        frame = cv2.resize(frame, (0,0), fx=0.8, fy=0.8)
        #print frame.shape
        img = cv2.imencode('.jpg', frame)[1]
        byteArray = numpy.array(img).tostring()
        streamer.sendImage(byteArray)
