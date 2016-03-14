import socks  # SocksiPy module
import socket
import StringIO
import urllib
import stem.process
from stem.util import term
from message import Message
import StringIO
import pickle
SOCKS_PORT = 7000

HS_ID = 'ogok5j2jcrh2a5hg'
KEY_LOCATION = 'C:\Users\Martin\Tor\HiddenService\private_key'

# Set socks proxy and wrap the urllib module

socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', SOCKS_PORT)
socket.socket = socks.socksocket



def print_bootstrap_lines(line):
  if "Bootstrapped " in line:
    print(term.format(line, term.Color.BLUE))

tor_process = stem.process.launch_tor_with_config(
  config = {
    'SocksPort': str(SOCKS_PORT)
  },
  init_msg_handler = print_bootstrap_lines,
)

HOST = 'ag6ut2t6b725wezs.onion'    # The remote host
PORT = 80      # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
	s.connect((HOST, PORT))
	input = 'hello world'
	message = Message()
	message.setBody(input)
	message.setSender(HS_ID)
	message.sign(KEY_LOCATION)
	
	output = pickle.dumps(message, -1)
	print(str(len(output)))
	s.sendall(output)
	dings = raw_input()
except Exception as e:
	print('something went wrong: '+str(e))
finally:	
	s.close()
	tor_process.kill() 
