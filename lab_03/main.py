from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PIL import Image
from MyWindow import Ui_MainWindow
import numpy as np
import sys


path_photo, image = "", ""


def get_data(path_photo, tools=False):
    if path_photo == "":
        data, width, height = [], 0, 0
    else:
        image = Image.open(path_photo)
        width = image.size[0]
        height = image.size[1]
        data = np.array(image.convert("RGB"))
    
    return data, width, height if tools else data


def encode_char(data, char, x, y, remainder=0):
    ascii_char = ord(char)
    new_pixs, count = [], 0
    
    last_zero = 0b11111110
    
    one = 0b00000001
    zero = 0b0
    
    while ascii_char > 0 or count != 8:
        if ascii_char & one:
            new_pixs += [one]
        else:
            new_pixs += [zero]
        count += 1
        ascii_char >>= 1
        
    data[x, y][0] = data[x, y][0] & last_zero | new_pixs[0]
    data[x, y][1] = data[x, y][1] & last_zero | new_pixs[1]
    data[x, y][2] = data[x, y][2] & last_zero | new_pixs[2]
    
    if remainder == 1:
        data[x, y + 1][0] = data[x, y + 1][0] & last_zero | new_pixs[3]
        data[x, y + 1][1] = data[x, y + 1][1] & last_zero | new_pixs[4]
        data[x, y + 1][2] = data[x, y + 1][2] & last_zero | new_pixs[5]
        
        data[x + 1, zero][0] = data[x + 1, zero][0] & last_zero | new_pixs[6]
        data[x + 1, zero][1] = data[x + 1, zero][1] & last_zero | new_pixs[7]
    
    elif remainder == 2:
        data[x + 1, zero][0] = data[x + 1, zero][0] & last_zero | new_pixs[3]
        data[x + 1, zero][1] = data[x + 1, zero][1] & last_zero | new_pixs[4]
        data[x + 1, zero][2] = data[x + 1, zero][2] & last_zero | new_pixs[5]
        
        data[x + 1, one][0] = data[x + 1, one][0] & last_zero | new_pixs[6]
        data[x + 1, one][1] = data[x + 1, one][1] & last_zero | new_pixs[7]
    else:
        data[x, y + 1][0] = data[x, y + 1][0] & last_zero | new_pixs[3]
        data[x, y + 1][1] = data[x, y + 1][1] & last_zero | new_pixs[4]
        data[x, y + 1][2] = data[x, y + 1][2] & last_zero | new_pixs[5]
        
        data[x, y + 2][0] = data[x, y + 2][0] & last_zero | new_pixs[6]
        data[x, y + 2][1] = data[x, y + 2][1] & last_zero | new_pixs[7]


def decode_char(data, x, y, remainder=0):
    num_char = 0b00000000
    last_bit = 0b00000001
    
    if remainder == 1:
        num_char |= (data[x + 1, 0][1] & last_bit) << 7
        num_char |= (data[x + 1, 0][0] & last_bit) << 6
    
        num_char |= (data[x, y + 1][2] & last_bit) << 5
        num_char |= (data[x, y + 1][1] & last_bit) << 4
        num_char |= (data[x, y + 1][0] & last_bit) << 3
    
    elif remainder == 2:
        num_char |= (data[x + 1, 1][1] & last_bit) << 7
        num_char |= (data[x + 1, 1][0] & last_bit) << 6
        
        num_char |= (data[x + 1, 0][2] & last_bit) << 5
        num_char |= (data[x + 1, 0][1] & last_bit) << 4
        num_char |= (data[x + 1, 0][0] & last_bit) << 3
        
    else:
        num_char |= (data[x, y + 2][1] & last_bit) << 7
        num_char |= (data[x, y + 2][0] & last_bit) << 6
        
        num_char |= (data[x, y + 1][2] & last_bit) << 5
        num_char |= (data[x, y + 1][1] & last_bit) << 4
        num_char |= (data[x, y + 1][0] & last_bit) << 3
    
    num_char |= (data[x, y][2] & last_bit) << 2
    num_char |= (data[x, y][1] & last_bit) << 1
    num_char |= (data[x, y][0] & last_bit)
    
    return chr(num_char)


def encode_string(data, height, width, string):
    start, count, flag_len = 0, 0, False
    for x in range(height):
        for y in range(start, width - 2, 3):
            encode_char(data, string[count], x, y)
            if string[count] == "&":
                flag_len = True
                break                    
            count += 1
        if flag_len:
            break
        
        start = width - (y + 3)
        if start:
            start = 1 if start == 2 else 2
            encode_char(data, string[count], x, y + 3, remainder=start)
            if string[count] == "&":
                break
            count += 1
            
    return data


def decode_image(data, height, width):
    decode_text = str()
    flag_len, start, success = False, 0, 0
    for x in range(height):
        for y in range(start, width - 2, 3):
            decode_text += decode_char(data, x, y)
            if decode_text[-1] == "&":
                flag_len = True
                break
        if flag_len:
            break

        start = width - (y + 3)
        if start and x != height - 1:
            start = 1 if start == 2 else 2
            decode_text += decode_char(data, x, y + 3, remainder=start)
            if decode_text[-1] == "&":
                break
    else:
        success = 100
        
    return decode_text, success


class window(QtWidgets.QMainWindow):
    def __init__(self):
        super(window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.AddingPhoto.clicked.connect(self.GetPhoto)
        self.ui.HideButton.clicked.connect(self.EncodeMessage)
        self.ui.SaveButton.clicked.connect(self.SavePhoto)
        self.ui.action.triggered.connect(self.EncodeMessage)
        self.ui.action_2.triggered.connect(self.DecodeImage)
        self.ui.action_3.setShortcut("Ctrl+W")
        self.ui.action_3.triggered.connect(self.ClearAll)
        self.ui.Quit.setShortcut("Ctrl+D")
        self.ui.Quit.triggered.connect(QtWidgets.qApp.quit)
        self.ui.ExtractButton.clicked.connect(self.DecodeImage)
        
    def GetPhoto(self):
        global path_photo
        new_path = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите изображение", None, "*.bmp")[0]
        path_photo = new_path if new_path else path_photo
        if not path_photo:
            return
        pix = QPixmap(path_photo)
        if not pix.size().height() or not pix.size().width():
            self.ErrorDialog("Изображение не выбрано или оно некорректно. Повторите попытку")
            return
        proportion = pix.size().width() / pix.size().height()
        p = pix.scaled(int(400 * proportion), 400, aspectRatioMode=Qt.KeepAspectRatio)
        self.ui.PhotoFrame.setPixmap(p)

    def SavePhoto(self):
        global path_photo
        data = get_data(path_photo)[0]
        if len(data) == 0:
            self.ErrorDialog("Нет изображения для сохранения. Повторите попытку", btns=False)
            return
        new_image = Image.fromarray(data)
        name = QtWidgets.QFileDialog.getSaveFileName(filter="Image Files (*.bmp)")[0]
        if name == "":
            return
        new_image.save(name)
        path_photo = name
        
    def EncodeMessage(self):
        global path_photo
        
        if path_photo == "":
            self.ErrorDialog("Изображение для кодирования не выбрано. Попробуйте снова")
            return
            
        data, width, height = get_data(path_photo, tools=True)
        
        string = self.ui.TextEntry.toPlainText() + "&"
        if len(string) > width * height // 3:
            self.ErrorDialog("Строка для кодирования слишком большая. Попробуйте снова", btns=False)
            return
        
        data = encode_string(data, height, width, string)
            
        path_photo = path_photo.split("/")
        path_photo[-1] = "result.bmp"
        path_photo = "/".join(path_photo)
        
        new_image = Image.fromarray(data)
        new_image.save(path_photo)
        
        pix = QPixmap(path_photo)
        proportion = pix.size().width() / pix.size().height()
        p = pix.scaled(int(400 * proportion), 400, aspectRatioMode=Qt.KeepAspectRatio)
        self.ui.PhotoFrame.setPixmap(p)
        
    def DecodeImage(self):
        global path_photo
        
        if path_photo == "":
            self.ErrorDialog("Изображение для декодирования не выбрано. Попробуйте снова")
            return
        
        data, width, height = get_data(path_photo, tools=True)
        
        decode_text, success = decode_image(data, height, width)
            
        if success:
            self.ErrorDialog("Картинка не может быть раскодирована. Выберите другое изображение")
            return
            
        self.ui.ExEntry.setPlainText(decode_text[:-1])
        
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