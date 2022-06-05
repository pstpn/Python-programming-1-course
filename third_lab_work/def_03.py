# Информация о программе:
# 
# [ЗАЩИТА ЛАБОРАТОРНОЙ РАБОТЫ]
# 
# Программа, реализующая попиксельный XOR изображений одинакового размера
# Реализована в рамках курса по "Программированию на Python".
# 
# Автор: Постнов Степан Андреевич, студент МГТУ им. Н.Э.Баумана


from calendar import c
from cmath import pi
from os import stat
from tracemalloc import start
from turtle import goto, heading, width
import weakref
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PIL.ImageQt import ImageQt
from PIL import Image
from MyWindow_def import Ui_MainWindow
import numpy as np
import sys

path_photo_1, path_photo_2 = "", ""


def get_data(path_photo, tools=False):
    image = Image.open(path_photo)
    width = image.size[0]
    height = image.size[1]
    data = np.array(image.convert("RGB"))
    
    return data, width, height if tools else data


def xor_images(data_1, data_2, height, width):
    data = data_1
    
    for x in range(width):
        for y in range(height):
            data[x, y][0] ^= data_2[0][x][y][0]
            data[x, y][1] ^= data_2[0][x][y][1]
            data[x, y][2] ^= data_2[0][x][y][2]
            
    return data
    

class window(QtWidgets.QMainWindow):
    def __init__(self):
        super(window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.AddingPhoto.clicked.connect(self.GetPhoto_1)
        self.ui.AddingPhoto_2.clicked.connect(self.GetPhoto_2)
        self.ui.XORButton.clicked.connect(self.XORImgs)
        self.ui.Quit.setShortcut("Ctrl+D")
        self.ui.Quit.triggered.connect(QtWidgets.qApp.quit)
        
    def GetPhoto(self, num_2=False):
        path_photo = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите изображение", None, "*.bmp")[0]
        pix = QPixmap(path_photo)
        proportion = pix.size().width() / pix.size().height()
        p = pix.scaled(int(400 * proportion), 400, aspectRatioMode=Qt.KeepAspectRatio)
        if num_2:
            self.ui.PhotoFrame_2.setPixmap(p)
        else:
            self.ui.PhotoFrame.setPixmap(p)
        return path_photo
            
    def GetPhoto_1(self):
        global path_photo_1
        path_photo_1 = self.GetPhoto()
            
    def GetPhoto_2(self):
        global path_photo_2
        path_photo_2 = self.GetPhoto(num_2=True)
        
    def XORImgs(self):
        global path_photo_1
        data_1, width, height  = get_data(path_photo_1, tools=True)
        data_2 = get_data(path_photo_2)
        
        xor_data = xor_images(data_1, data_2, width, height)
        
        path_photo = path_photo_1.split("/")
        path_photo[-1] = "result.bmp"
        path_photo = "/".join(path_photo)
        
        new_image = Image.fromarray(xor_data)
        new_image.save(path_photo)
        
    def ErrorDialog(self, info, btns=True):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        
        msg.setText("Ошибка")
        msg.setInformativeText(info)
        msg.setWindowTitle("Error")
        if btns:
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Open)
        else:
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            
        msg.buttonClicked.connect(self.ControlAction)
        
        msg.exec_()
    
    def ControlAction(self, btn):
        if btn.text() == "Open":
            self.GetPhoto()
            
    def ClearAll(self):
        self.ui.TextEntry.clear()
        self.ui.ExEntry.clear()
        

class Img(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.toggleStyle()

    def clearPixmap(self):
        super().clear()

    def toggleStyle(self):
        self.setText("\n\nМесто для изображения\n\n")
        self.setStyleSheet('''
            QLabel {
                color: grey;
                font: 20pt;
            }
        ''')


app = QtWidgets.QApplication([])
application = window()
application.show()
 
sys.exit(app.exec())