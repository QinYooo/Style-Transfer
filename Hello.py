# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Hello.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(871, 631)
        self.base_weiget = QtWidgets.QWidget(MainWindow)
        self.base_weiget.setObjectName("base_weiget")
        self.widget = QtWidgets.QWidget(self.base_weiget)
        self.widget.setGeometry(QtCore.QRect(10, 10, 851, 591))
        self.widget.setObjectName("widget")
        self.widget_2 = QtWidgets.QWidget(self.widget)
        self.widget_2.setGeometry(QtCore.QRect(10, 40, 811, 531))
        self.widget_2.setObjectName("widget_2")
        self.btn_pause = QtWidgets.QPushButton(self.widget_2)
        self.btn_pause.setGeometry(QtCore.QRect(530, 490, 111, 41))
        self.btn_pause.setObjectName("btn_pause")
        self.btn_capture = QtWidgets.QPushButton(self.widget_2)
        self.btn_capture.setGeometry(QtCore.QRect(350, 490, 121, 41))
        self.btn_capture.setObjectName("btn_capture")
        self.btn_input = QtWidgets.QPushButton(self.widget_2)
        self.btn_input.setGeometry(QtCore.QRect(180, 490, 121, 41))
        self.btn_input.setObjectName("btn_input")
        self.btn_style = QtWidgets.QPushButton(self.widget_2)
        self.btn_style.setGeometry(QtCore.QRect(10, 490, 121, 41))
        self.btn_style.setObjectName("btn_style")
        self.label_video = QtWidgets.QLabel(self.widget_2)
        self.label_video.setGeometry(QtCore.QRect(10, 0, 760, 480))
        self.label_video.setMinimumSize(QtCore.QSize(760, 480))
        self.label_video.setMaximumSize(QtCore.QSize(760, 480))
        self.label_video.setText("")
        self.label_video.setObjectName("label_video")
        self.widget_3 = QtWidgets.QWidget(self.widget)
        self.widget_3.setGeometry(QtCore.QRect(10, 10, 111, 31))
        self.widget_3.setObjectName("widget_3")
        self.hide = QtWidgets.QPushButton(self.widget_3)
        self.hide.setGeometry(QtCore.QRect(30, 7, 16, 16))
        self.hide.setMinimumSize(QtCore.QSize(16, 16))
        self.hide.setMaximumSize(QtCore.QSize(16, 16))
        self.hide.setText("")
        self.hide.setObjectName("hide")
        self.close = QtWidgets.QPushButton(self.widget_3)
        self.close.setGeometry(QtCore.QRect(10, 7, 16, 16))
        self.close.setMinimumSize(QtCore.QSize(16, 16))
        self.close.setMaximumSize(QtCore.QSize(16, 16))
        self.close.setText("")
        self.close.setObjectName("close")
        MainWindow.setCentralWidget(self.base_weiget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btn_pause.setText(_translate("MainWindow", "??????"))
        self.btn_capture.setText(_translate("MainWindow", "???????????????"))
        self.btn_input.setText(_translate("MainWindow", "??????????????????"))
        self.btn_style.setText(_translate("MainWindow", "??????????????????"))
