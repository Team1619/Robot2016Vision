import socket
import time

import random

import json

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('127.0.0.1', 5801))

print 'listening'
sock.listen(1)

conn, addr = sock.accept()
print 'Accepted', str(conn), str(addr)

i = 0

conn.send(json.dumps({
    'type': 'currentValues',
    'longs': {},
    'doubles': {},
    'strings': {}}) + '\n')

while True:
    time.sleep(1)
    conn.send(json.dumps({'type':'updateLong', 'key':'innerBallSensor', 'value':random.randrange(0, 2)}) + '\n')
    conn.send(json.dumps({'type':'updateLong', 'key':'outerBallSensor', 'value':random.randrange(0, 2)}) + '\n')
    conn.send(json.dumps({'type':'updateDouble', 'key':'heading', 'value':round(random.random() * 360, 3)}) + '\n')
    conn.send(json.dumps({'type':'updateDouble', 'key':'distance', 'value':round(random.random() * 250, 3)}) + '\n')
    conn.send(json.dumps({'type':'updateLong', 'key':'shooterSpeed', 'value':random.randrange(0, 30001)}) + '\n')
    i += 1
    print 'hi'

conn.close()
sock.close()
