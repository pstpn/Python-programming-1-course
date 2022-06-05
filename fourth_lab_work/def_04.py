# Множество точек. Треугольник с наим площадью
# Информация о программе:
# 
# [ЗАЩИТА ЛАБОРАТОРНОЙ РАБОТЫ]
# 
# Программа ищет треугольник с наименьшей площадью среди всех введенных вручную
# Реализован в рамках курса по "Программированию на Python".
# 
# Автор: Постнов Степан Андреевич, студент МГТУ им. Н.Э.Баумана


from calendar import c
from cmath import pi
from os import stat
import re
from secrets import choice
from tracemalloc import start
from turtle import goto, heading, right, width
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QGridLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PIL.ImageQt import ImageQt
from PIL import Image
from MyWindow_def import Ui_MainWindow
import numpy as np
import sys


colors = [
'#FFFF00', '#FF00FF', '#00BFFF', '#E0FFFF', '#FF0000', '#00FF7F',
'#ADFF2F', '#C71585', '#FFD700', '#F5DEB3', '#00FF00', '#a15c3e', '#a42f3b',
'#f45b7a', '#c24998', '#81588d', '#bcb0c2', '#ffffff',
]


def get_square(x1, y1, x2, y2, x3, y3):
    return 0.5 * abs((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1))
    

def get_triangle(coordinates):
    len_coords = len(coordinates)
    
    coord_min = [(coordinates[0][0], coordinates[0][1]),
                 (coordinates[1][0], coordinates[1][1]),
                 (coordinates[2][0], coordinates[2][1])]
    
    min_square = get_square(coordinates[0][0], coordinates[0][1], \
                            coordinates[1][0], coordinates[1][1], \
                            coordinates[2][0], coordinates[2][1])
    
    for num, coord in enumerate(coordinates):
        x1, y1 = coord[0], coord[1]
        for j in range(num + 1, len_coords):
            x2, y2 = coordinates[j][0], coordinates[j][1]
            for z in range(j + 1, len_coords):
                x3, y3 = coordinates[z][0], coordinates[z][1]
                square = get_square(x1, y1, x2, y2, x3, y3)
                if square < min_square:
                    coord_min[0] = (x1, y1)
                    coord_min[1] = (x2, y2)
                    coord_min[2] = (x3, y3)
                    min_square = square
    
    return coord_min


class window(QtWidgets.QMainWindow):
    def __init__(self):
        super(window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.SetCoordinates()
        
        self.ui.FindTriangles.clicked.connect(self.DrawAnswer)
        self.ui.ClearGraph.clicked.connect(self.DeleteGraph)
        
        self.ui.Finding.triggered.connect(self.DrawAnswer)
        self.ui.Quit.setShortcut("Ctrl+D")
        self.ui.Clear_btn.triggered.connect(self.DeleteGraph)
        self.ui.Clear_btn.setShortcut("Ctrl+W")
        self.ui.Quit.triggered.connect(QtWidgets.qApp.quit)
        
        self.coordinates = []
        
        
    def SetCoordinates(self):
        canvas = QtGui.QPixmap(720, 720)
        self.ui.label.setPixmap(canvas)

        self.last_x, self.last_y = None, None
        
        
    def mousePressEvent(self, e):
        painter = QtGui.QPainter(self.ui.label.pixmap())
        p = painter.pen()
        p.setWidth(6)
        p.setColor(QtGui.QColor(choice(colors)))
        painter.setPen(p)
        painter.drawPoint(e.pos().x() - 12, e.pos().y() - 116)
        
        self.coordinates += [(e.pos().x() - 12, e.pos().y() - 116)]
        
        painter.end()
        self.update()
        
        return super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        self.last_x = None
        self.last_y = None
        
        
    def DrawAnswer(self):
        if not self.coordinates:
            self.ErrorDialog("Координаты не были заданы. Попробуйте снова")
            return
        
        coord = get_triangle(self.coordinates)
        
        if not coord:
            self.ErrorDialog("Треугольник, удовлетворяющий условию, не был найден. Попробуйте снова")
            return
        
        painter = QtGui.QPainter(self.ui.label.pixmap())
        pen = QtGui.QPen()
        pen.setWidth(3)
        pen.setColor(QtGui.QColor("green"))
        painter.setPen(pen)
        
        painter.drawLine(
            QtCore.QPoint(*coord[0]),
            QtCore.QPoint(*coord[1])
        )
        painter.drawLine(
            QtCore.QPoint(*coord[1]),
            QtCore.QPoint(*coord[2])
        )
        painter.drawLine(
            QtCore.QPoint(*coord[2]),
            QtCore.QPoint(*coord[0])
        )
        
        self.ui.label.update()
        painter.end()  
    
    
    def DeleteGraph(self):
        self.ui.label.pixmap().fill(QtCore.Qt.black)
        self.ui.label.update()
        
        self.coordinates = []
        
    def ClearAll(self):
        self.DeleteGraph()
        self.coordinates = []
        
    def ErrorDialog(self, info):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        
        msg.setText("Ошибка")
        msg.setInformativeText(info)
        msg.setWindowTitle("Error")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        
        msg.exec_()  
        
        
app = QtWidgets.QApplication([])
application = window()
application.show()

sys.exit(app.exec())