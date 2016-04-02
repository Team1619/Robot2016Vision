
import sys
import traceback
import errno

import socket
import json
import time
import threading
from autobahn.asyncio.websocket import WebSocketServerProtocol, WebSocketServerFactory
import trollius

import numbers

class DriverStationProtocol(WebSocketServerProtocol):

    def onOpen(self):
        self.factory.register(self)

    def onMessage(self, payLoad):
        self.factory.fuckYourselfAndYourDonkey()

    def onClose(self, wasClean, code, reason):
        self.factory.unregister(self)

class SmashBoard(WebSocketServerFactory):

    protocol = DriverStationProtocol
    BUFFER_SIZE = 4096

    def __init__(self, url='ws://127.0.0.1:5000', host='localhost', port=1619):
        WebSocketServerFactory.__init__(self, url)
        self.clients = []

        self.socket = socket.socket()
        #self.socket.settimeout(1)
        self.host = host
        self.port = port
        self.longMap = {}
        self.doubleMap = {}
        self.stringMap = {}
        self.updateThread = threading.Thread(target=self.__listenOnSocket)
        self.runThread = False

    def cleanUp(self):
        print 'Cleaning up'
        print self.longMap, self.doubleMap, self.stringMap
        self.runThread = False
        while self.updateThread.isAlive():
            pass
        self.socket.sendall(json.dumps({
            'type': 'disconnect'
            }) + '\n')
        self.socket.close()

    def connectAndStartUpdateThread(self):
        self.runThread = True
        self.updateThread.start()

    def register(self, client):
        if client not in self.clients:
            self.clients.append(client)
            print 'Registered client {}'.format(client.peer)
            client.sendMessage(json.loads({'type':'connected'}), False)

    def unregister(self, client):
        if clients in self.clients:
            self.clients.remove(client)
            print 'Unregistered client {}'.format(client.peer)

    def updateValue(self, message):
        for client in self.clients:
            client.sendMessage(message, False)

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

    def __connect(self):
        print 'Trying to connect to {}:{}'.format(self.host, self.port)
        try:
            self.socket.connect((self.host, self.port))
        except socket.error as e:
            errorCode = e[0]
            if errorCode != errno.ECONNREFUSED:
                traceback.print_exc()
            print 'Not connected'
            self.socket.close()
            self.socket = socket.socket()
            return False
        print 'Connected'
        return True

    # method which is target of updateThread
    def __listenOnSocket(self):
        while self.runThread:
            while not self.__connect() and self.runThread:
                time.sleep(1)
            try:
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
                        traceback.print_exc()
                        print 'Data not in expected format or does not contain expected values: \n' + data
            except IOError:
                traceback.print_exc()
            finally:
                self.socket.close()
                self.socket = socket.socket()
                print 'Disconnected from server'
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
                traceback.print_exc()
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
    smashBoard = SmashBoard(host='192.168.1.126', port=5801)
    print 'Hello'
    smashBoard.connectAndStartUpdateThread()
    loop = trollius.get_event_loop()
    coro = loop.create_server(smashBoard, '127.0.0.1', 5000)
    server = loop.run_until_complete(coro)


    try:
        loop.run_forever()
        #while 1:
        #    time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        loop.close()
        smashBoard.cleanUp()
        print 'Goodbye'
