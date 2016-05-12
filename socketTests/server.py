import socket
import time


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 5556))
s.listen(1)
s, addr = s.accept()
print(s.getpeername())
time.sleep(2)
s.shutdown(socket.SHUT_RDWR)
s.close()