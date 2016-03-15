import socket
import pickle
from message import Message

HOST = ''
PORT = 55555

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(1)
con, addr = sock.accept()

print('connected')
try:
	while 1:
		d =con.recv(32)
		if len(d)==0:
			break
		messageLen = int(d[:4].decode('ascii'))
		d = d[4:]
		messageLen = int(messageLen)
		while 1:
			if len(d)<messageLen:
				d+=con.recv(min(1024, messageLen-len(d)))
			else:
				break
		if '---stop---' == d:
			break
		message = pickle.loads(d)
		print('message from: '+ message.sender)
		print(message.body)
		status = message.checkSignature()
		if status:
			print('status: CORRECT')
		else:
			print('status: NOT VERIFIED!!')
		print(' ')

finally:
	print('shutting down!')
	con.shutdown(socket.SHUT_RDWR)
	con.close()
