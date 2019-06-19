import sys
import time
import re
import random
import threading
import inspect
import ctypes

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtGui

def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)

class Heap_Sort(QWidget):
    time = 0.05
    inputs1 = 0
    inputs2 = 0
    isend = -1
    def __init__(self):
        super().__init__()
        window_pale = QtGui.QPalette()
        window_pale.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap("heapSort_back.jpg")))
        self.setPalette(window_pale)
        self.setWindowTitle("归并排序")
        self.setFixedSize(950, 700)

        self.paintarea = PaintArea(self)
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.paintarea)
        sub_layout = QHBoxLayout()
        sub_layout.setContentsMargins(10, 10, 10, 10)

        self.combobox_1 = QComboBox(self)
        self.combobox_1.addItem("自动输入")
        self.combobox_1.addItem("手动输入")
        self.combobox_1.currentIndexChanged.connect(self.clicked1)
        sub_layout.addWidget(self.combobox_1)

        self.lineEdit = QLineEdit()
        self.lineEdit.setParent(self)
        self.lineEdit.returnPressed.connect(self.prepare)
        sub_layout.addWidget(self.lineEdit)

        self.dial = QDial(self)
        self.dial.setNotchesVisible(True)
        self.dial.setRange(0, 100)
        self.dial.valueChanged.connect(self.speed)
        sub_layout.addWidget(self.dial)
        pe = QPalette()
        pe.setColor(QPalette.WindowText, Qt.white)  # 设置字体颜色
        self.lable = QLabel("速度:0")
        self.lable.setPalette(pe)
        sub_layout.addWidget(self.lable)

        self.combobox_2 = QComboBox(self)
        self.combobox_2.addItem("连续运行")
        self.combobox_2.addItem("单步运行")
        self.combobox_2.currentIndexChanged.connect(self.clicked2)
        sub_layout.addWidget(self.combobox_2)

        self.start = QPushButton("开始")
        self.start.setParent(self)
        self.start.clicked.connect(self.run)
        sub_layout.addWidget(self.start)

        self.stop = QPushButton("暂停")
        self.stop.setParent(self)
        self.stop.clicked.connect(self.pause)
        sub_layout.addWidget(self.stop)

        self.restart = QPushButton("继续")
        self.restart.setParent(self)
        self.restart.clicked.connect(self.resume)
        sub_layout.addWidget(self.restart)

        self.step = QPushButton("单步")
        self.step.setParent(self)
        self.step.clicked.connect(self.steps)
        sub_layout.addWidget(self.step)
        main_layout.addLayout(sub_layout)
        self.show()
    def speed(self):
        self.lable.setText("速度:" + str(self.dial.value()))
        self.time=0.05-0.0004*(self.dial.value())

    def Exchange(self,first,second):
        self.paintarea.flag=1
        self.paintarea.remove.append(first)
        self.paintarea.remove.append(second)
        self.paintarea.num=[self.datas[first],self.datas[second]]
        x1=self.paintarea.circle[first][0]
        y1=self.paintarea.circle[first][1]
        x2 = self.paintarea.circle[second][0]
        y2 = self.paintarea.circle[second][1]
        y=(y2-y1)/30
        x=(x2-x1)/30
        if self.inputs2:
            self.step_single.clear()
            self.step_single.wait()
        for i in range(30):
            self.singal.wait()
            x1=x1+x
            y1=y1+y
            x2=x2-x
            y2=y2-y
            self.paintarea.move=[x1,y1,x2,y2]
            self.paintarea.repaint()
            time.sleep(self.time)

        temp = self.datas[second]
        self.datas[second] = self.datas[first]
        self.datas[first] = temp
        self.paintarea.datas = self.datas
        self.paintarea.flag = 0
        self.paintarea.remove=[]
        self.paintarea.num=[]

    def HeapAdjust(self,parent, length):

        child = 2 * parent + 1
        while child < length:
            temp = self.datas[parent]
            if child + 1 < length and self.datas[child] < self.datas[child + 1]:
                child += 1
            if temp > self.datas[child]:
                break
            self.Exchange(parent,child)
            parent = child
            child = 2 * child + 1


    def HeapSort(self):
        # 调整parent结点为大根堆
        if self.datas == []:
            return []
        length = len(self.datas)
        # 最后一个结点的下标为length//2-1
        # 建立初始大根堆
        for i in range(0, length // 2)[::-1]:
            self.HeapAdjust( i, length)

        for j in range(1, length)[::-1]:
            self.paintarea.line = j
            self.Exchange(0,j)
            self.HeapAdjust( 0, j)

    def begin(self):
        self.isend = 0
        self.HeapSort()
        self.isend = 1
        self.paintarea.repaint()

    def clicked1(self):
        self.inputs1=self.combobox_1.currentIndex()

    def clicked2(self):
        self.inputs2 = self.combobox_2.currentIndex()

    def prepare(self):
        self.datas=[]
        flag=0
        str=self.lineEdit.text()
        if self.inputs1 == 1:
            an = re.search('^\d+(,\d+)*$',str)
            if an:
                var = str.split(',')
                if len(var)<=15 and len(str)>=1:
                    for i in var:
                        if int(i)==0 or int(i)>99:
                            flag=1
                            QMessageBox.information(self, "警告", "非法数值", QMessageBox.Yes)
                    if flag == 0:
                        for i in var:
                            self.datas.append(int(i))
                else:
                    QMessageBox.information(self, "警告", "非法长度", QMessageBox.Yes)
            else:
                QMessageBox.information(self,"警告", "非法格式",QMessageBox.Yes)
        else:
            an = re.search('^[1-9]\d*$', str)
            if an:
                if  int(str)>15:
                    QMessageBox.information(self, "警告", "非法数值", QMessageBox.Yes)
                else:
                    for i in range(int(str)):
                        self.datas.append(random.randint(1, 99))
            else:
                QMessageBox.information(self,"警告", "非法格式",QMessageBox.Yes)
        self.paintarea.datas = self.datas
        self.paintarea.line=len(self.datas)
        self.paintarea.repaint()

    def run(self):
        if self.inputs2 :
            self.step_single= threading.Event()
        self.singal = threading.Event()
        self.singal.set()
        self.t = threading.Thread(target=self.begin)
        self.t.start()

    def pause(self):
        self.singal.clear()

    def resume(self):
        self.singal.set()

    def steps(self):
        self.step_single.set()

    def closeEvent(self, event):
        if self.isend==0:
            stop_thread(self.t)

class PaintArea(QWidget):
    datas=[]
    line = len(datas)
    flag = 0
    remove=[]
    circle=[[403, 30],[173, 180],[633, 180],[58, 330],[288, 330],[518, 330],[748, 330],[0, 480],[115, 480],[230, 480],[345, 480],[460, 480],[575, 480],[690, 480],[805, 480]]
    lines=[[410, 110, 265, 200],[495, 110, 640, 200],[185, 270, 140, 340],[260, 270, 305, 340],[645, 270, 600, 340],[720, 270, 765, 340],[85, 430, 60, 480],[131, 430, 155, 480],[315, 430, 290, 480],[361, 430, 385, 480],[545, 430, 520, 480],[591, 430, 615, 480],[775, 430, 750, 480],[821, 430, 845, 480]]
    def paintEvent(self,paintEvent):
        qp = QPainter()
        qp.begin(self)
        self.draw(qp)
        qp.end()

    def draw(self,qp):

        qp.setBrush(QColor(200, 200, 200))
        qp.setPen(QPen(QColor(255,0, 0), 4))
        qp.setFont(QFont('Decorative', 20))
        for i in range(len(self.datas)):
            if i not in self.remove:
                qp.drawEllipse(self.circle[i][0],self.circle[i][1],100,100)
                qp.drawText(self.circle[i][0]+35, self.circle[i][1]+60, str(self.datas[i]))
            if i>0 and i<self.line:
                qp.drawLine(self.lines[i-1][0], self.lines[i-1][1], self.lines[i-1][2], self.lines[i-1][3])

        if  self.flag==1:
            qp.setBrush(QColor(100, 100, 0))
            qp.setPen(QPen(QColor(0, 255, 0), 4))
            qp.setFont(QFont('Decorative', 20))
            qp.drawEllipse(self.move[0], self.move[1], 100, 100)
            qp.drawText(self.move[0] + 35, self.move[1] + 60, str(self.num[0]))
            qp.drawEllipse(self.move[2], self.move[3], 100, 100)
            qp.drawText(self.move[2] + 35, self.move[3] + 60, str(self.num[1]))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    heapsort = Heap_Sort()
    app.exec_()