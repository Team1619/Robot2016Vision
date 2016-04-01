import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('192.168.1.170', 5801))

print 'listening'
sock.listen(1)

conn, addr = sock.accept()
print 'Accepted', str(conn), str(addr)

conn.close()
sock.close()
