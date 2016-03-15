#import socks  # SocksiPy module
import socket
import stem.process
from stem.util import term
from message import Message
import pickle
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

	HOST = 'localhost'    # The remote host
	PORT = 55555      # The same port as used by the server

	def __init__(self, flav):
		HS_ID = ''
		path = ''
		if flav == 1:
			path = '/var/lib/tor/other_hidden_service/hostname'
		else:
			path = '/var/lib/tor/hidden_service/hostname'
		with open(path,'r') as f:
			HS_ID = f.read().split('.')[0]


		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			res = s.connect((HOST, PORT))
			if res!=0:
				sock.bind((HOST, PORT))
				sock.listen(1)
				con, addr = sock.accept()
			while 1:
				m_in = input()
				if m_in == '---stop---':
					s.sendall(m_in)
					break
				message = Message()
				message.setBody(m_in)
				message.setSender(HS_ID)
				message.sign()
				output = pickle.dumps(message, -1)
				#calculate length of message and pad to four digits
				length = str(len(output))
				if len(length) > 4:
					raise Exception('MessageLenException', 'this message is too long')
				length = ''.join(['0' for x in range(4-len(length))])+length
				s.sendall(length.encode('ascii')+output)

		finally:	
			s.shutdown(socket.SHUT_RDWR)
			s.close()
		#	tor_process.kill() 
