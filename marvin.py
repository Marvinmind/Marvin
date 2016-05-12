# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'marvin.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Marvin(object):
    def setupUi(self, Marvin):
        Marvin.setObjectName("Marvin")
        Marvin.resize(492, 335)
        self.centralwidget = QtWidgets.QWidget(Marvin)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.listView = QtWidgets.QListView(self.centralwidget)
        self.listView.setObjectName("listView")
        self.verticalLayout_3.addWidget(self.listView)
        self.verticalLayout_2.addLayout(self.verticalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_2.addWidget(self.lineEdit)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        Marvin.setCentralWidget(self.centralwidget)
        self.actionEdit_Contacts = QtWidgets.QAction(Marvin)
        self.actionEdit_Contacts.setObjectName("actionEdit_Contacts")

        self.retranslateUi(Marvin)
        QtCore.QMetaObject.connectSlotsByName(Marvin)

    def retranslateUi(self, Marvin):
        _translate = QtCore.QCoreApplication.translate
        Marvin.setWindowTitle(_translate("Marvin", "Marvin"))
        self.pushButton.setText(_translate("Marvin", "Send"))
        self.actionEdit_Contacts.setText(_translate("Marvin", "Edit Contacts"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Marvin = QtWidgets.QMainWindow()
    ui = Ui_Marvin()
    ui.setupUi(Marvin)
    Marvin.show()
    sys.exit(app.exec_())

