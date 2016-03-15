import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from marvin import Ui_Marvin

class MyFirstGuiProgram(Ui_Marvin):
	def __init__(self, dialog):
		Ui_Marvin.__init__(self)
		self.setupUi(dialog)

		# Connect "add" button with a custom function (addInputTextToListbox)
		self.pushButton.clicked.connect(self.addInputTextToListbox)

	def addInputTextToListbox(self):
		txt = self.lineEdit.text()
		self.listWidget.addItem(txt)

if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	dialog = QtWidgets.QDialog()
	prog = MyFirstGuiProgram(dialog)
	dialog.show()
	sys.exit(app.exec_())