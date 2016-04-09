import sys
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from marvin import Ui_Marvin
from socketClient import MarvinSock
from threading import Thread
import atexit
import message


class TestGUI(Ui_Marvin):
	def __init__(self, dialog):
		Ui_Marvin.__init__(self)
		self.setupUi(dialog)
		# Connect "add" button with a custom function (addInputTextToListbox)
		self.pushButton.clicked.connect(self.addToChat)

		self.chatListModel = QtGui.QStandardItemModel()
		self.listView.setModel(self.chatListModel)
	
	def addToChat(self):
			m_string = 'Sender: Mart\nBody: Hello world'
			item = QtGui.QStandardItem(m_string)
			item2 = QtGui.QStandardItem(m_string)

			#item.setForeground(QtGui.QColor('red'))
			self.chatListModel.appendRow(item)
			self.chatListModel.appendRow(item2)


if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	dialog = QtWidgets.QWidget()
	prog = TestGUI(dialog)
	dialog.show()
	sys.exit(app.exec_())