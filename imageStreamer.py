
import socket
import time

class ImageStreamer:

    def __init__(self, host='localhost', port=1619):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host = host
        self.port = port

    # takes plain image byte data
    def sendImage(self, imageData):
        self.socket.sendto(imageData + '\n', (self.host, self.port))

if __name__ == '__main__':
    streamer = ImageStreamer()
    while True:
        time.sleep(1)
        streamer.sendImage('hello')
