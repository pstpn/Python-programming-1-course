from secrets import choice
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
from MyWindow_4 import Ui_MainWindow
import sys


colors = [
'#FFFF00', '#FF00FF', '#00BFFF', '#E0FFFF', '#FF0000', '#00FF7F',
'#ADFF2F', '#C71585', '#FFD700', '#F5DEB3', '#00FF00', '#a15c3e', '#a42f3b',
'#f45b7a', '#c24998', '#81588d', '#bcb0c2', '#ffffff',
]


def is_straight(x1, y1, x2, y2, x3, y3):
    s = 0.5 * abs((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1))
    if 0 <= s <= 0:  # abs(s) <= eps
        return True
    return False


def is_convex(x1, y1, x2, y2, x3, y3, xp, yp):
    all_coords = [[x1, y1, x2, y2, x3, y3, xp, yp], 
                  [x1, y1, x2, y2, xp, yp, x3, y3],
                  [x1, y1, xp, yp, x3, y3, x2, y2],
                  [xp, yp, x2, y2, x3, y3, x1, y1]]
    
    for cur_coords in all_coords:
        x1, y1, x2, y2, x3, y3, xp, yp = cur_coords[0], cur_coords[1], \
        cur_coords[2], cur_coords[3], cur_coords[4], cur_coords[5], cur_coords[6], cur_coords[7]
        
        inter_counting_1 = (x1 - xp) * (y2 - y1) - (x2 - x1) * (y1 - yp)
        inter_counting_2 = (x2 - xp) * (y3 - y2) - (x3 - x2) * (y2 - yp)
        inter_counting_3 = (x3 - xp) * (y1 - y3) - (x1 - x3) * (y3 - yp)

        if (inter_counting_1 < 0 and inter_counting_2 < 0 and inter_counting_3 < 0) or \
            (inter_counting_1 > 0 and inter_counting_2 > 0 and inter_counting_3 > 0):
            return True

    return False
    
    
def is_intersect(x1, y1, x2, y2, x3, y3, x4, y4):
    first_1 = (x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1);
    second_1 = (x2 - x1) * (y4 - y1) - (x4 - x1) * (y2 - y1);

    result_1 = first_1 * second_1;

    first_2 = (x4 - x3) * (y1 - y3) - (x1 - x3) * (y4 - y3);
    second_2 = (x4 - x3) * (y2 - y3) - (x2 - x3) * (y4 - y3);

    result_2 = first_2 * second_2;
    
    if result_1 < 0 and result_2 < 0:
        return True
    
    return False


def finding_convexs(coordinates):
    
    data = []
    len_coords = len(coordinates)
    
    for num, coord in enumerate(coordinates):
        for j in range(num + 1, len_coords):
            x2, y2 = coordinates[j][0], coordinates[j][1]
            for k in range(j + 1, len_coords):
                x3, y3 = coordinates[k][0], coordinates[k][1]
                if not is_straight(coord[0], coord[1], x2, y2, x3, y3):
                    for z in range(k + 1, len_coords):
                        xp, yp = coordinates[z][0], coordinates[z][1]
                        if not is_convex(coord[0], coord[1], x2, y2, x3, y3, xp, yp):
                            if not is_intersect(coord[0], coord[1], xp, yp, x3, y3, x2, y2):
                                if not is_intersect(coord[0], coord[1], x2, y2, x3, y3, xp, yp):
                                    data += [[[coord[0], coord[1]], [x2, y2], [x3, y3], [xp, yp]]]
                                else:
                                    data += [[[coord[0], coord[1]], [x3, y3], [x2, y2], [xp, yp]]]
                            else:
                                data += [[[coord[0], coord[1]], [x2, y2], [xp, yp], [x3, y3]]]
                num += 1
            num += 1
    
    return data


class window(QtWidgets.QMainWindow):
    def __init__(self):
        super(window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.SetTable()
        
        self.SetCoordinates()
        
        self.ui.Clear.clicked.connect(self.ClearAll)
        self.ui.FindFigures.clicked.connect(self.DrawAnswer)
        self.ui.ClearGraph.clicked.connect(self.DeleteGraph)
        
        self.ui.ClearAll_2.setShortcut("Ctrl+W")
        self.ui.ClearAll_2.triggered.connect(self.ClearAll)
        self.ui.Finding.triggered.connect(self.DrawAnswer)
        self.ui.Quit.setShortcut("Ctrl+D")
        self.ui.Quit.triggered.connect(QtWidgets.qApp.quit)
        
        self.coordinates = []
        
    def SetCoordinates(self):
        canvas = QtGui.QPixmap(720, 720)
        self.ui.label.setPixmap(canvas)

        self.last_x, self.last_y = None, None
        
    def SetTable(self):
        self.ui.table.setColumnCount(2)
        self.ui.table.setRowCount(100)
        
        self.ui.table.setColumnWidth(0, 180)
        self.ui.table.setColumnWidth(1, 180)
 
        self.ui.table.setHorizontalHeaderLabels(["X", "Y"])
 
        self.ui.table.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft)
        self.ui.table.horizontalHeaderItem(1).setTextAlignment(Qt.AlignLeft)
        
    def DataCompletion(self):
        for row in range(self.ui.table.rowCount()):
            first_elem, second_elem = self.ui.table.item(row, 0), self.ui.table.item(row, 1)
            if first_elem is not None and second_elem is not None:
                try:
                    int(first_elem.text()), int(second_elem.text())
                except:
                    continue
                if int(first_elem.text()) == float(first_elem.text()) and \
                    int(second_elem.text()) == float(second_elem.text()):
                    self.coordinates += [(int(first_elem.text()), int(second_elem.text()))]
                    
    def DrawAnswer(self):
        
        self.DataCompletion()
        
        if not self.coordinates:
            self.ErrorDialog("Координаты не были заданы. Попробуйте снова")
            return
        
        data = finding_convexs(self.coordinates)
        
        if not data:
            self.ErrorDialog("Четырехугольники, удовлетворяющие условию, не были найдены. Попробуйте снова")
            return
        
        painter = QtGui.QPainter(self.ui.label.pixmap())
        pen = QtGui.QPen()
        pen.setWidth(3)
        pen.setColor(QtGui.QColor("white"))
        painter.setPen(pen)
        
        for coord in data:
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
                QtCore.QPoint(*coord[3])
            )
            painter.drawLine(
                QtCore.QPoint(*coord[3]),
                QtCore.QPoint(*coord[0])
            )
        
        self.ui.label.update()
        painter.end()
    
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
        
    def DeleteAllTableData(self):
        for column in range(self.ui.table.columnCount()):
            for row in range(self.ui.table.rowCount()):
                if self.ui.table.item(row, column) is not None:
                    self.ui.table.item(row, column).setText("")
                    
    def DeleteGraph(self):
        self.ui.label.pixmap().fill(QtCore.Qt.black)
        self.ui.label.update()
        
        self.coordinates = []
        self.DataCompletion()
        
    def ClearAll(self):
        self.DeleteAllTableData()
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