import sys
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from marvin import Ui_Marvin
from test import Ui_MainWindow
from socketClient import ServerSock, ClientSock
from threading import Thread
from contacts import Contacts
import atexit
from messageSimple import Message
from queue import Queue


class RecThread(QThread):
    receive_signal = pyqtSignal(Message)

    def __init__(self, sock):
        QThread.__init__(self)
        self.sock = sock

    def run(self):
        while 1:
            m = self.sock.receive_message()
            if m:
                print('emit message')
                self.receive_signal.emit(m)


class SendThread(QThread):
    def __init__(self, sock, queue):
        QThread.__init__(self)
        self.sock = sock
        self.queue = queue

    def run(self):
        while 1:
            val= self.queue.get()
            if val is not None:
                self.sock.send_message(val)


class ListenThread(QThread):
    #Define a signal that emits a new Client Sock
    incoming_connection_signal = pyqtSignal(ClientSock)

    def __init__(self, port):
        QThread.__init__(self)
        self.serverSock = ServerSock(port)

    def run(self):
        while 1:
            conn = self.serverSock.getConnection()
            self.clientSock = ClientSock(serverPort)
            self.clientSock.s = conn
            print('connection established')

            self.incoming_connection_signal.emit(self.clientSock)

        #win = ConvWindow(socket=self.clientSock)
        #win.show()


class ConvWindow(QtWidgets.QMainWindow, Ui_Marvin):
    def __init__(self, **kwargs):
        super(ConvWindow, self).__init__(None)
        self.setupUi(self)

        #Check if socket hat been given. If not create socket from address.
        if 'sock' in kwargs:
            print('socket transfered')
            self.sock = kwargs['sock']
        else:
            self.sock = ClientSock(serverPort)
            self.sock.connect(int(kwargs['addr']))

        #Set up sender thread
        self.queue = Queue()
        self.send_thread = SendThread(self.sock, self.queue)
        self.send_thread.start()

        #Set up receiver thread
        self.get_thread = RecThread(self.sock)
        self.get_thread.start()
        self.get_thread.receive_signal.connect(self.addToChat)

        self.pushButton.clicked.connect(self.sendMessage)
        self.pushButton.clicked.connect(self.lineEdit.clear)

        self.chatListModel = QtGui.QStandardItemModel()
        self.listView.setModel(self.chatListModel)

    def addToChat(self, m):
        m_string = 'From: {}\nMessage: \n{}\nStatus: {}\n'.format(m.sender,m.body, m.verify())
        item = QtGui.QStandardItem(m_string)
        item.setForeground(QtGui.QColor('red'))
        self.chatListModel.appendRow(item)

    def sendMessage(self):
        message = self.lineEdit.text()
        item = QtGui.QStandardItem(str(message)+'\n')
        item.setForeground(QtGui.QColor('blue'))
        self.chatListModel.appendRow(item)
        self.queue.put(message)


class Main(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Main, self).__init__(None)
        self.setupUi(self)

        self.listenThread = ListenThread(serverPort)
        self.listenThread.start()
        self.listenThread.incoming_connection_signal.connect(lambda x: self.openConversation(sock=x))

        self.convWindows = []
        self.contacts = Contacts(clientNumber).contacts
        for c in self.contacts:
            el = ''
            if 'name' in c:
                el = c['name']
            elif 'address' in c:
                el = c['address']
            if el != '':
                item = self.listWidget.addItem(el)
        self.listWidget.itemDoubleClicked.connect(lambda: self.openConversation(addr=c['address']))

    def openConversation(self, **kwargs):
        if 'sock' in kwargs:
            self.win = ConvWindow(sock=kwargs['sock'])

        elif 'addr' in kwargs:
            if not kwargs['addr'] in self.convWindows:
                addr = kwargs['addr']
                self.convWindows.append(addr)
                self.win = ConvWindow(addr=addr)

        self.win.show()

if __name__ == '__main__':
    try:
        app = QtWidgets.QApplication(sys.argv)
        clientNumber = int(sys.argv[1])

        if clientNumber==1:
            serverPort=5555
        elif clientNumber == 2:
            serverPort=5556
        else:
            serverPort=5557

        prog = Main()
        prog.show()
        sys.exit(app.exec_())
    finally	:
        pass
    #if socket:
    #	socket.kill_sock()
