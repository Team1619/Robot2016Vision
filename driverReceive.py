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

while True:
    time.sleep(1)
    conn.send(json.dumps({'type':'updateString', 'key':'theString', 'value':'hi'}) + '\n')
    print 'hi'

conn.close()
sock.close()
