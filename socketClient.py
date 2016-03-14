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
	print('start rec')
	d = con.recv(520, socket.MSG_WAITALL)
	print('end rec, length'+str(len(d)))
	con.shutdown(socket.SHUT_RDWR)
	con.close()

	message = pickle.loads(d)
	print('pickled')
	print('message body: '+ message.body)
	print('message sender: '+ message.sender)
	status = message.checkSignature()
	if status:
		print('signature is correct')
	else:
		print('incorrect signature')
except Exception as e:
	print(e)
finally:
	print('shutting down!')
