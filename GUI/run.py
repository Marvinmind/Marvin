import sys
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QThread, SIGNAL
from marvin import Ui_Marvin
from socketClient import MarvinSock
from threading import Thread


class RecThread(QThread, socket):
	def __init__(self):
		QThread.__init__(self)

	def run(self):
		while 1:
			m = socket.receive_message()
			self.emit(SIGNAL('add_post(QString)'), m)

class MyFirstGuiProgram(Ui_Marvin):
	def __init__(self, dialog,socket):
		Ui_Marvin.__init__(self)
		self.setupUi(dialog)

		# Connect "add" button with a custom function (addInputTextToListbox)
		self.pushButton.clicked.connect(self.sendMessage)

		self.get_thread = RecThread(subreddit_list,socket)
		self.connect(self.get_thread, SIGNAL("add_post(QString)"), self.addToChat)

	def addToChat(self, message):
		self.listWidget.addItem(message)
	def sendMessage(self, message):
		message = self.lineEdit.text()
		t = Thread(target=socket.sendMessage, args=(message,))
		t.start()

if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	dialog = QtWidgets.QDialog()
	socket = MarvinSock(sys.argv[2])
	prog = MyFirstGuiProgram(dialog)
	dialog.show()
	sys.exit(app.exec_())