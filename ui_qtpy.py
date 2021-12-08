#!/usr/bin/env python3.5
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QImage, QIcon, QPixmap
from PyQt5.QtCore import QTimer
from subprocess import call
import cv2


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon('Logo of Digit Recognition.ico'))
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.control_bt1.clicked.connect(self.load_project)
        self.ui.control_bt2.clicked.connect(self.Digit_rgn)
        self.ui.control_bt3.clicked.connect(self.takedata)


    def load_project(self):
        print("Loading Hand Gesture Digit Recognition System...")
        call(["python3","1project.py"])

    def Digit_rgn(self):
        print("Loading Hand Written Digit Recognition System...")
        call(["python3","digitrecognition.py"])

    def takedata(self):
        print("Loading Create DataSet...")
        call(["python3","takedata.py"])

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(800, 500)
        self.bg = QtWidgets.QLabel(Form)
        self.bg.setObjectName("bg")
        self.bg.setGeometry(0,0,800,500)
        self.bg.setStyleSheet("QLabel {image: url(images/background.png)}")

        self.de = QtWidgets.QLabel(Form)
        self.de.setObjectName("de")
        self.de.setGeometry(40,350,350,40)
        self.de.setText("<font color='green' font size=5 font face='arial'>Team Members:</font>")

        self.kiitlogo = QtWidgets.QLabel(Form)
        self.kiitlogo.setObjectName("kiitlogo")
        self.kiitlogo.setGeometry(650,20,100,100)
        self.kiitlogo.setStyleSheet("QLabel {image: url(images/kiitlogo.png)}")

        self.details1 = QtWidgets.QLabel(Form)
        self.details1.setObjectName("details1")
        self.details1.setGeometry(40,380,500,40)
        self.details1.setText("<font color='white' font size=5 font face='arial'>Anand Kumar &nbsp; Anish Hota &nbsp; Champak Sinha</font>")

        self.details2 = QtWidgets.QLabel(Form)
        self.details2.setObjectName("details2")
        self.details2.setGeometry(40,410,350,40)
        self.details2.setText("<font color='white' font size=5 font face='arial'>Pranesh Biswas &nbsp; Rishab</font>")

        self.details3 = QtWidgets.QLabel(Form)
        self.details3.setObjectName("details3")
        self.details3.setGeometry(40,440,350,40)
        self.details3.setText("<font color='green' font size=5 font face='arial'>Guide: Prof. Sushruta Mishra</font>")

        self.control_bt1 = QtWidgets.QPushButton(Form)
        self.control_bt1.setObjectName("control_bt1")
        self.control_bt1.setGeometry(40,150,200,200)
        self.control_bt1.setStyleSheet("QPushButton {image: url(images/bt_1_black.png)}"
                                        "QPushButton {border-radius: 10px}"
                                        "QPushButton {background-color: black}"
                                        "QPushButton:pressed {image: url(images/bt_1_green.png)}"
                                        "QPushButton:hover:!pressed {image: url(images/bt_1_grey.png)}")
        self.control_bt2 = QtWidgets.QPushButton(Form)
        self.control_bt2.setObjectName("control_bt2")
        self.control_bt2.setGeometry(300,150,200,200)
        self.control_bt2.setStyleSheet("QPushButton {image: url(images/bt_2_black.png)}"
                                        "QPushButton {border-radius: 10px}"
                                        "QPushButton {background-color: black}"
                                        "QPushButton:pressed {image: url(images/bt_2_green.png)}"
                                        "QPushButton:hover:!pressed {image: url(images/bt_2_grey.png)}")
        self.control_bt3 = QtWidgets.QPushButton(Form)
        self.control_bt3.setObjectName("control_bt3")
        self.control_bt3.setGeometry(560,150,200,200)
        self.control_bt3.setStyleSheet("QPushButton {image: url(images/bt_3_black.png)}"
                                        "QPushButton {border-radius: 10px}"
                                        "QPushButton {background-color: black}"
                                        "QPushButton:pressed {image: url(images/bt_3_green.png)}"
                                        "QPushButton:hover:!pressed {image: url(images/bt_3_grey.png)}")
        #self.gif_1 = QtGui.QMovie()
        #self.gif_1.setGeometry()

        self.retranslateUi(Form)
        #QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(translate("Form", "Digit Recognition System"))
        #self.control_bt1.setText(translate("Form", "Open Digit Gesture Recognition System"))
        #self.control_bt2.setText(translate("Form", "Open Hand Written Digit Recognition System"))
        #self.control_bt3.setText(translate("Form", "Create DataSet"))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    mainWindow = MainWindow()
    mainWindow.show()
    mainWindow.setFixedSize(800,500)
    sys.exit(app.exec_())
