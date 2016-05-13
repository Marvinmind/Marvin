#import socks  # SocksiPy module
import socket
import stem.process
from stem.util import term
from messageSimple import Message, MessageCreator
import pickle
import sys
from threading import Thread
import time

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
            self.path = '/var/lib/tor/other_hidden_service'
        else:
            self.path = '/var/lib/tor/hidden_service'

        self.gen = MessageCreator(self.path)

        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            res = self.s.connect_ex((self.HOST, self.PORT))
            if res!=0:
                self.s.bind((self.HOST, self.PORT))
                self.s.listen(1)
                self.s, addr = self.s.accept()
        finally:
            pass
        #finally:
        #	s.shutdown(socket.SHUT_RDWR)
        #	s.close()
        #	tor_process.kill()

    def receive_message(self):
        d = self.s.recv(32)
        if len(d)==0:
            return
        print('something came in')
        messageLen = int(d[:4].decode('ascii'))
        d = d[4:]
        messageLen = int(messageLen)
        while 1:
            if len(d)<messageLen:
                d+=self.s.recv(min(1024, messageLen-len(d)))
            else:
                break
        if '---stop---' == d:
            return
        message = pickle.loads(d)
        return message

    def send_message(self, m_in):
        message = self.gen.buildMessage(m_in, self.sPort)
        output = pickle.dumps(message, -1)
        #calculate length of message and pad to four digits
        length = str(len(output))
        if len(length) > 4:
            raise Exception('MessageLenException', 'this message is too long')
        length = ''.join(['0' for x in range(4-len(length))])+length
        print('goes out!')
        self.s.sendall(length.encode('ascii')+output)

    def send_worker(self):
        while 1:
            m = input()
            if m == '---end---':
                kill_sock()
            else:
                self.send_message(m)
    def receive_worker(self):
        while 1:
            m = self.receive_message()
            if m == '---end---':
                kill_sock()
            print(m.body)
    def kill_sock(self):
        self.s.shutdown(socket.SHUT_RDWR)
        self.s.close()


class ClientSock(MarvinSock):
    def __init__(self, sPort):
        self.gen = MessageCreator(sPort)
        self.sPort = sPort

    def connect(self, cPort):
        self.cPort = cPort
        try:
            conStatus = 1
            while conStatus != 0:
                time.sleep(1)
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                conStatus = self.s.connect_ex(('localhost', self.cPort))

            newPort = self.s.recv(32)
            newPort = newPort.decode('ascii')
            print('new Port is:'+ newPort)
            self.s.close()
            conStatus = 1

            while conStatus != 0:
                time.sleep(1)
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                conStatus = self.s.connect_ex(('localhost', int(newPort)))
            print('leavin connection est')
            return True
        except Exception as e:
            print(e)
            self.kill_sock()


class ServerSock(MarvinSock):
    nextPort = 5705

    def get_Port(self):
        return self._lastUsedPort

    def set_Port(self, port):
        self._lastUsedPort = port

    def __init__(self, port):
        self.port = port
        self.gen = MessageCreator(port)
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.bind(('localhost', self.port))
            self.s.listen(5)
        except Exception:
            raise e

    def getConnection(self):
        #try:
            conn, addr = self.s.accept()
            #Create new Socket for the interested party
            temp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            temp_sock.bind(('localhost', ServerSock.nextPort))
            conn.sendall(str(ServerSock.nextPort).encode('ascii'))
            temp_sock.listen(10)
            connTemp, addrTemp = temp_sock.accept()
            ServerSock.nextPort+=1

            #Kick party from server sock and reacreate sock
            self.s.listen(5)
            return connTemp

if __name__ == '__main__':
    marvsock = MarvinSock(int(sys.argv[1]))
    t_rec = Thread(target=marvsock.receive_worker)
    r_send = Thread(target=marvsock.send_worker)
    threads = [t_rec, r_send]
    for t in threads:
        t.start()
    for x in threads:
        x.join()
