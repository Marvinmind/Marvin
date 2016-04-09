import sys
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from marvin import Ui_Marvin
from test import Ui_MainWindow
from socketClient import MarvinSock
from threading import Thread
import atexit
import message

class RecThread(QThread):
	receive_signal = pyqtSignal(message.Message)
	def __init__(self):
		QThread.__init__(self)

	def run(self):
		while 1:
			m = socket.receive_message()
			self.receive_signal.emit(m)

class MyFirstGuiProgram(Ui_Marvin):
	def __init__(self, dialog,socket):
		Ui_Marvin.__init__(self)
		self.setupUi(dialog)
		# Connect "add" button with a custom function (addInputTextToListbox)
		self.pushButton.clicked.connect(self.sendMessage)
		self.pushButton.clicked.connect(self.lineEdit.clear)

		self.get_thread = RecThread()
		self.get_thread.start()
		self.get_thread.receive_signal.connect(self.addToChat)

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
		t = Thread(target=socket.send_message, args=(message,))
		t.start()

class Main(Ui_MainWindow):
	def __init__(self, dialog):
		self.setupUi.__init__(self)
		self.setupUi(dialog)
		self.pushButton.clicked.connect(self.openConversation)

	def openConversation(self):
		window = MyFirstGuiProgram(self)
		window.show()

if __name__ == '__main__':
#	try:
		app = QtWidgets.QApplication(sys.argv)
		dialog = QtWidgets.QMainWindow()
	#	print(sys.argv[1])
	#	socket = MarvinSock(int(sys.argv[1]))
#		prog = MyFirstGuiProgram(dialog, socket)
		prog = Main(dialog)
		dialog.show()
		sys.exit(app.exec_())
#	finally:
#		if socket:
#			socket.kill_sock()
#atexit.register(socket.kill_sock())