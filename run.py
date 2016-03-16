import sys
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from marvin import Ui_Marvin
from socketClient import MarvinSock
from threading import Thread


class RecThread(QThread):
	receive_signal = pyqtSignal(str)
	def __init__(self):
		QThread.__init__(self)

	def run(self):
		while 1:
			m = socket.receive_message()
			self.receive_signal.emit(m.body)

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

	def addToChat(self, message):
		self.listWidget.addItem(message)
	def sendMessage(self, message):
		message = self.lineEdit.text()
		self.listWidget.addItem(message)
		t = Thread(target=socket.send_message, args=(message,))
		t.start()

if __name__ == '__main__':
	try:
		app = QtWidgets.QApplication(sys.argv)
		dialog = QtWidgets.QWidget()
		print(sys.argv[1])
		socket = MarvinSock(int(sys.argv[1]))
		prog = MyFirstGuiProgram(dialog, socket)
		dialog.show()
		sys.exit(app.exec_())
	finally:
		if socket:
			socket.kill_sock()