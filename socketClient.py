#import socks  # SocksiPy module
import socket
import stem.process
from stem.util import term
from message import Message
import pickle
import sys
from threading import Thread

SOCKS_PORT = 7000

# Set socks proxy and wrap the urllib module

#socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', SOCKS_PORT)
#socket.socket = socks.socksocket

def print_bootstrap_lines(line):
  if "Bootstrapped " in line:
    print(term.format(line, term.Color.BLUE))

#tor_process = stem.process.launch_tor_with_config(
#  config = {
#    'SocksPort': str(SOCKS_PORT)
#  },
#  init_msg_handler = print_bootstrap_lines,
#)

class MarvinSock():
	def __init__(self, flav):
		self.HOST = 'localhost'    # The remote host
		self.PORT = 55555      # The same port as used by the server
		
		if flav == 1:
			path = '/var/lib/tor/other_hidden_service/hostname'
		else:
			path = '/var/lib/tor/hidden_service/hostname'
		with open(path,'r') as f:
			self.HS_ID = f.read().split('.')[0]
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			res = s.connect_ex((self.HOST, self.PORT))
			if res!=0:
				s.bind((self.HOST, self.PORT))
				s.listen(1)
				s, addr = s.accept()
		finally:
			pass
		#finally:	
		#	s.shutdown(socket.SHUT_RDWR)
		#	s.close()
		#	tor_process.kill() 
	def receive_message(self):
		d =s.recv(32)
		if len(d)==0:
			return
		messageLen = int(d[:4].decode('ascii'))
		d = d[4:]
		messageLen = int(messageLen)
		while 1:
			if len(d)<messageLen:
				d+=s.recv(min(1024, messageLen-len(d)))
			else:
				break
		if '---stop---' == d:
			return
		message = pickle.loads(d)
		return message

	def send_message(self, message):
		m_in = input()
		if m_in == '---stop---':
			s.sendall(m_in)
			return
		message = Message()
		message.setBody(m_in)
		message.setSender(self.HS_ID)
		message.sign()
		output = pickle.dumps(message, -1)
		#calculate length of message and pad to four digits
		length = str(len(output))
		if len(length) > 4:
			raise Exception('MessageLenException', 'this message is too long')
		length = ''.join(['0' for x in range(4-len(length))])+length
		s.sendall(length.encode('ascii')+output)

	def send_worker(self):
		while 1:
			m = input()
			if m == '---end---':
				kill_sock()
			else:
				send_message(m)
	def receive_worker(self):
		while 1:
			m = receive_message()
			if m == '---end---':
				kill_sock()
			print(message.body)
	def kill_sock(self):
		s.shutdown(socket.SHUT_RDWR)
		s.close()


if __name__ == '__main__':
	marvsock = MarvinSock(int(sys.argv[1]))
	t_rec = Thread(target=receive_worker)
	r_send = Thread(target=send_worker)
