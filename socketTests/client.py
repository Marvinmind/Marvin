import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
res = s.connect_ex(('localhost', 5556))
print(s.getpeername())