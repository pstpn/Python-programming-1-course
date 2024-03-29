# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MyWindow_4.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1166, 877)
        MainWindow.setStyleSheet("background-color: rgb(46, 52, 54);\n"
"color: rgb(243, 243, 243);\n"
"font: 63 13pt \"URW Gothic\";")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.FindFigures = QtWidgets.QPushButton(self.centralwidget)
        self.FindFigures.setGeometry(QtCore.QRect(740, 750, 411, 61))
        self.FindFigures.setStyleSheet("background-color: rgb(46, 52, 54);\n"
"color: rgb(243, 243, 243);\n"
"font: 63 14pt \"URW Gothic\";")
        self.FindFigures.setObjectName("FindFigures")
        self.table = QtWidgets.QTableWidget(self.centralwidget)
        self.table.setGeometry(QtCore.QRect(740, 80, 411, 651))
        self.table.setObjectName("table")
        self.table.setColumnCount(0)
        self.table.setRowCount(0)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 90, 720, 720))
        self.label.setMaximumSize(QtCore.QSize(720, 720))
        self.label.setText("")
        self.label.setObjectName("label")
        self.ClearGraph = QtWidgets.QPushButton(self.centralwidget)
        self.ClearGraph.setGeometry(QtCore.QRect(110, 10, 351, 61))
        self.ClearGraph.setStyleSheet("background-color: rgb(46, 52, 54);\n"
"color: rgb(243, 243, 243);\n"
"font: 63 14pt \"URW Gothic\";")
        self.ClearGraph.setObjectName("ClearGraph")
        self.Clear = QtWidgets.QPushButton(self.centralwidget)
        self.Clear.setGeometry(QtCore.QRect(630, 10, 351, 61))
        self.Clear.setStyleSheet("background-color: rgb(46, 52, 54);\n"
"color: rgb(243, 243, 243);\n"
"font: 63 14pt \"URW Gothic\";")
        self.Clear.setObjectName("Clear")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1166, 23))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        MainWindow.setMenuBar(self.menubar)
        self.ClearAll = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("URW Bookman")
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.ClearAll.setFont(font)
        self.ClearAll.setObjectName("ClearAll")
        self.Quit = QtWidgets.QAction(MainWindow)
        self.Quit.setObjectName("Quit")
        self.ClearAll_2 = QtWidgets.QAction(MainWindow)
        self.ClearAll_2.setObjectName("ClearAll_2")
        self.Finding = QtWidgets.QAction(MainWindow)
        self.Finding.setObjectName("Finding")
        self.menu.addAction(self.ClearAll_2)
        self.menu.addAction(self.Finding)
        self.menu_2.addAction(self.Quit)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.FindFigures.setText(_translate("MainWindow", "Найти четырехугольники"))
        self.ClearGraph.setText(_translate("MainWindow", "Очистить граф. поле"))
        self.Clear.setText(_translate("MainWindow", "Очистить все"))
        self.menu.setTitle(_translate("MainWindow", "Инструменты"))
        self.menu_2.setTitle(_translate("MainWindow", "Выход"))
        self.ClearAll.setText(_translate("MainWindow", "Очистить все поля"))
        self.Quit.setText(_translate("MainWindow", "Выход"))
        self.ClearAll_2.setText(_translate("MainWindow", "Очистить все"))
        self.Finding.setText(_translate("MainWindow", "Найти четырехугольники"))
