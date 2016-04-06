
import socket
import json
import time
import threading

import numbers

class SmashBoard:

    BUFFER_SIZE = 4096

    def __init__(self, host='localhost', port=1619):
        self.socket = socket.socket()
        self.socket.settimeout(1)
        self.host = host
        self.port = port
        self.longMap = {}
        self.doubleMap = {}
        self.stringMap = {}
        self.updateThread = threading.Thread(target=self.__listenOnSocket)
        self.runThread = False

    def connect(self):
        self.socket.connect((self.host, self.port))

    def cleanUp(self):
        print 'cleaning up'
        print self.longMap, self.doubleMap, self.stringMap
        self.runThread = False
        while self.updateThread.isAlive():
            pass
        self.socket.sendall(json.dumps({
            'type': 'disconnect'
            }) + '\n')
        self.socket.close()

    def startUpdateThread(self):
        self.runThread = True
        self.updateThread.start()

    def __send(self, message):
        self.socket.sendall(json.dumps(message) + '\n')

    # generic setValue for sending accross socket
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

    # method which is target of updateThread
    def __listenOnSocket(self):
        for line in self.__readLines(self.socket, self.BUFFER_SIZE):
            #print line
            data = json.loads(line)
            try:
                if data['type'] == 'updateLong':
                    #print 'updated long: ' + data['key']
                    self.longMap[data['key']] = data['value']
                elif data['type'] == 'updateDouble':
                    #print 'updated double: ' + data['key']
                    self.doubleMap[data['key']] = data['value']
                elif data['type'] == 'updateString':
                    #print 'updated string: ' + data['key']
                    self.stringMap[data['key']] = data['value']
                elif data['type'] == 'currentValues':
                    self.longMap = data['longs']
                    self.doubleMap = data['doubles']
                    self.stringMap = data['strings']
            except:
                print 'Data not in expected format or does not contain expected values: \n' + data
        return

    def __readLines(self, socket, recvBuffer, delimiter='\n'):
        buffer = ''
        data = True
        while data and self.runThread:
            try:
                data = socket.recv(recvBuffer)
                buffer += data

                while buffer.find(delimiter) != -1:
                    line, buffer = buffer.split(delimiter, 1)
                    yield line
            except:
                pass
        return

    def setLong(self, key, value):
        if isinstance(value, numbers.Number):
            self.__setValue(key, value, 'setLong')
        else:
            print 'Not a number'

    def setDouble(self, key, value):
        if isinstance(value, numbers.Number):
            self.__setValue(key, value, 'setDouble')
        else:
            print 'Not a number'

    def setString(self, key, value):
        if isinstance(value, basestring):
            self.__setValue(key, value, 'setString')
        else:
            print 'Not a string'

    def getLong(self, key):
        try:
            return self.longMap[key]
        except:
            print 'Key: ' + key + ' does not exist in longMap'

    def getDouble(self, key):
        try:
            return self.doubleMap[key]
        except:
            print 'Key: ' + key + ' does not exist in doubleMap'

    def getString(self, key):
        try:
            return self.stringMap[key]
        except:
            print 'Key: ' + key + ' does not exist in stringMap'

if __name__ == '__main__':
    smashBoard = SmashBoard(host='10.16.19.2', port=1619)
    #smashBoard = SmashBoard(port=8000)
    smashBoard.connect()
    smashBoard.startUpdateThread()

    print 'Hello'
    i = 0.1
    j = 0
    while 1:
        message = raw_input('Message: ')
        if message != 'Q':
            smashBoard.setDouble('message', i)
            smashBoard.setLong('message3', j)
            smashBoard.setString('message2', message)
        else:
            smashBoard.cleanUp()
            break

        i = i + 1
        j = j + 1

    print 'Goodbye'
