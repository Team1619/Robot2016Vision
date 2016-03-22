
import socket
import time
import numpy
import cv2

#from flask import Flask, render_template, Response

class ImageReceiver:

    BUFFER_SIZE = 65535

    def __init__(self, host='192.168.1.126', port=1619):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.host = host
        self.port = port
        self.socket.bind((self.host, self.port))
        #self.app = Flask(__name__)
        #@self.app.route('/')
        #def index():
        #    return render_template('index.html')

        #@self.app.route('/video_feed')
        #def video_feed():
        #    return Response(self.gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

    # takes plain image byte data
    def receiveImage(self):
        return self.socket.recvfrom(self.BUFFER_SIZE)[0]

    def gen(self):
        while True:
            frame = self.receiveImage()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    #def run(self):
    #    self.app.run(host='localhost', debug=True)

if __name__ == '__main__':
    receiver = ImageReceiver()
    while True:
        data = receiver.receiveImage()
        img = numpy.fromstring(data, dtype=numpy.uint8)
        frame = cv2.imdecode(img, 1)
        frame = frame[:,::-1,:]
        cv2.imshow('img', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
