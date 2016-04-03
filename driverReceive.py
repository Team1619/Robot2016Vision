import socket
import time

import json

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('192.168.1.126', 5801))

print 'listening'
sock.listen(1)

conn, addr = sock.accept()
print 'Accepted', str(conn), str(addr)

i = 0

conn.send(json.dumps({
    'type': 'currentValues',
    'longs': {'initLong': 1},
    'doubles': {},
    'strings': {'initString': 'lol'}}) + '\n')

while True:
    time.sleep(1)
    conn.send(json.dumps({'type':'updateString', 'key':'theString', 'value':'hi'}) + '\n')
    conn.send(json.dumps({'type':'updateLong', 'key':'theLong', 'value':i}) + '\n')
    i += 1
    print 'hi'

conn.close()
sock.close()
