
import socket
import json
import time
import threading

import numbers

class SmashBoard:

    BUFFER_SIZE = 4096

    def __init__(self, host='localhost', port=1619):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.numberMap = {}
        self.stringMap = {}
        self.updateThread = threading.Thread(target=self.__listenOnSocket)
        self.runThread = 0

    def connect(self):
        self.socket.connect_ex((self.host, self.port))

    def cleanUp(self):
        self.runThread = 0
        while self.updateThread.isAlive():
            pass
        self.socket.close()

    def startUpdateThread(self):
        self.runThread = 1
        self.updateThread.start()

    def __send(self, message):
        self.socket.send(json.dumps(message) + '\n')

    def __setValue(self, key, value, valueType):
        if not isinstance(key, basestring):
            print 'Key must be of type string'
            return
        if not isinstance(valueType, basestring):
            print 'valueType must be of type string'
            return
        message = {
            'type': valueType,
            'key': key,
            'value': value
        }

        self.__send(message)

    def __listenOnSocket(self):
        while self.runThread:
            data = json.loads(str(self.socket.recv(BUFFER_SIZE)))
            try:
                if data['type'] == 'updateNumber':
                    self.numberMap[data['key']] = data['value']
                elif data['type'] == 'updateString':
                    self.stringMap[data['key']] = data['value']
                elif data['type'] == 'updateAll':
                    self.numberMap.update(data['numberMap'])
                    self.stringMap.update(data['stringMap'])
            except:
                print 'Data not in expected format or does not contain expected values: \n' + data

    def setNumber(self, key, value):
        if isinstance(value, numbers.Number):
            self.__setValue(key, value, 'setNumber')
        else:
            print 'Not a number'

    def setString(self, key, value):
        if isinstance(value, basestring):
            self.__setValue(key, value, 'setString')
        else:
            print 'Not a string'

    def getString(self, key):
        try:
            return self.stringMap[key]
        except:
            print 'Key: ' + key + ' does not exist in stringMap'

    def getNumber(self, key):
        try:
            return self.numberMap[key]
        except:
            print 'Key: ' + key + ' does not exist in numberMap'

if __name__ == '__main__':
    smashBoard = SmashBoard(host='192.168.1.158', port=1619)
    smashBoard.connect()
    smashBoard.startUpdateThread()

    print 'Hello'
    i = 0
    while 1:
        message = raw_input('Message: ')
        if message != 'Q':
            smashBoard.setNumber('message', i)
            smashBoard.setString('message2', message)
        else:
            smashBoard.cleanUp()
            break

        i = i + 1

    print 'Goodbye'
