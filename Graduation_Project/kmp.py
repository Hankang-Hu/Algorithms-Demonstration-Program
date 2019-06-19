import sys
import time
import re
import threading
import inspect
import ctypes
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

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

class KMP(QWidget):
    time = 0.5
    inputs2 = 0
    isend = -1
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KMP算法")
        self.setFixedSize(950, 700)

        self.paintarea = PaintArea(self)
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.paintarea)
        sub_layout = QHBoxLayout()
        sub_layout.setContentsMargins(10, 10, 10, 10)


        self.lineEdit = QLineEdit()
        self.lineEdit.setParent(self)
        self.lineEdit.returnPressed.connect(self.prepare)
        sub_layout.addWidget(self.lineEdit)

        self.dial = QDial(self)
        self.dial.setNotchesVisible(True)
        self.dial.setRange(0, 100)
        self.dial.valueChanged.connect(self.speed)
        sub_layout.addWidget(self.dial)
        self.lable = QLabel("速度:0")
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

    def KMP_algorithm(self,string, substring):
        '''
        KMP字符串匹配的主函数
        若存在字串返回字串在字符串中开始的位置下标，或者返回-1
        '''
        pnext = self.gen_pnext(substring)
        n = len(string)
        m = len(substring)
        i, j = 0, 0
        while (i < n) and (j < m):
            if (string[i] == substring[j]):
                self.paintarea.removeup.append(i)
                self.paintarea.removedown.append(j)
                i += 1
                j += 1
            elif (j != 0):
                j = pnext[j - 1]
                self.paintarea.removedown = []
                self.paintarea.removeup = []
            else:
                i += 1
            self.paintarea.i2 = i
            self.paintarea.j2 = j
            time.sleep(self.time)
            self.paintarea.repaint()
            if self.inputs2 == 1:
                self.singal.clear()
            else:
                time.sleep(self.time)
            self.singal.wait()
        if (j == m):
            return i - j
        else:
            return -1

    def gen_pnext(self,substring):  #构造临时数组pnext
        j, length,i = 0, len(substring),1
        pnext = [0] * length
        self.paintarea.flag = 1
        self.paintarea.pnext = pnext
        self.paintarea.i1=i
        self.paintarea.j1=j
        while i < length:
            if (substring[i] == substring[j]):
                self.paintarea.removedown.append(i)
                self.paintarea.removedown.append(j)
                pnext[i] = j + 1
                j += 1
                i += 1
            elif (j != 0):
                j = pnext[j - 1]
                self.paintarea.removedown=[]
            else:
                pnext[i] = 0
                i += 1
            self.paintarea.pnext = pnext
            self.paintarea.i1 = i
            self.paintarea.j1 = j
            time.sleep(self.time)
            self.paintarea.repaint()
            if self.inputs2 == 1:
                self.singal.clear()
            else:
                time.sleep(self.time)
            self.singal.wait()
        self.paintarea.removedown = []
        self.paintarea.flag = 0
        return pnext

    def begin(self):
        self.isend = 0
        result=self.KMP_algorithm(self.string,self.substring)
        self.paintarea.result=result
        self.isend = 1


    def clicked2(self):
        self.inputs2 = self.combobox_2.currentIndex()

    def prepare(self):
        str=self.lineEdit.text()
        an = re.search('^[0-9A-Za-z][0-9A-Za-z]*,[0-9A-Za-z][0-9A-Za-z]*$',str)
        if an:
            var = str.split(',')
            if len(var[0])>=6 and len(var[0])<=20 and len(var[1])<=len(var[0]):
                self.string=var[0]
                self.substring=var[1]
                self.paintarea.string = self.string
                self.paintarea.substring = self.substring
                self.paintarea.flag = 0
                self.paintarea.i2=0
                self.paintarea.j2 = 0
                self.paintarea.pnext = []
                self.paintarea.removeup = []
                self.paintarea.removedown = []
            else:
                QMessageBox.information(self, "警告", "非法长度", QMessageBox.Yes)
        else:
            QMessageBox.information(self,"警告", "非法格式",QMessageBox.Yes)
        self.paintarea.repaint()


    def run(self):
        self.singal = threading.Event()
        if self.inputs2==0:
            self.singal.set()
        self.t = threading.Thread(target=self.begin)
        self.t.start()
        #self.begin()


    def pause(self):
        self.singal.clear()

    def resume(self):
        self.singal.set()

    def steps(self):
        self.singal.set()

    def closeEvent(self, event):
        if self.isend==0:
            stop_thread(self.t)

class PaintArea(QWidget):
    string = ''
    substring =''
    flag=0
    pnext=[]
    removeup=[]
    removedown=[]
    i2=0
    j2=0
    result=-2
    def __init__(self, Parent=None):
        super().__init__(Parent)
        self.setPalette(QPalette(Qt.white))  # 背景颜色
        self.setAutoFillBackground(True)  # 设置窗体自动填充背景
        self.setFixedSize(950, 600)

    def paintEvent(self,paintEvent):
        qp = QPainter()
        qp.begin(self)
        self.draw(qp)
        qp.end()

    def draw(self,qp):
        if len(self.string)>0:
            length = 900 / len(self.string)
        else: length=0
        qp.setBrush(QColor(255, 255, 0))
        qp.setPen(QColor(0, 0, 0))
        qp.setFont(QFont('Decorative', length * 0.65))
        for i in range(len(self.string)):
            if i not in self.removeup:
                qp.drawRect(length * i, 70, length, length)
                qp.drawText(length * i + length * 0.2, 70 + length * 0.9, self.string[i])
        for i in range(len(self.substring)):
            if i not in self.removedown:
                qp.drawRect(length * (i+self.i2-self.j2), 140 + length, length, length)
                qp.drawText(length * (i+self.i2-self.j2) + length * 0.2, 140 + length * 1.9, self.substring[i])
        qp.setBrush(QColor(255, 255, 255))
        for i in range(len(self.pnext)):
            qp.drawRect(length * (i+self.i2-self.j2), 140 + length * 2, length, length)
            qp.drawText(length * (i+self.i2-self.j2) + length * 0.2, 140 + length * 2.9, str(self.pnext[i]))
        qp.setBrush(QColor(0, 255, 0))

        for i in range(len(self.removeup)):
            qp.drawRect(length * self.removeup[i], 70, length, length)
            qp.drawText(length * self.removeup[i] + length * 0.2, 70 + length * 0.9, self.string[self.removeup[i]])

        for i in range(len(self.removedown)):
            qp.drawRect(length * (self.removedown[i]+self.i2-self.j2), 140 + length, length, length)
            qp.drawText(length * (self.removedown[i]+self.i2-self.j2) + length * 0.2, 140 + length * 1.9, self.substring[self.removedown[i]])

        if self.flag==1:
            qp.setPen(QPen(QColor(255, 0, 0), 4))
            qp.setFont(QFont('Decorative',40))
            qp.drawLine(length * self.i1+0.5*length, 80 + length,length * self.i1+0.5*length, 140 + length)
            qp.drawText(length * self.i1+0.5*length, 130 + length, 'i')
            qp.drawLine(length * self.j1 + 0.5 * length, 80 + length, length * self.j1 + 0.5 * length, 140 + length)
            qp.drawText(length * self.j1 + 0.5 * length, 130 + length, 'j')
        if self.result==-1:
            QMessageBox.information(self, "结果", "匹配失败", QMessageBox.Yes)
            self.result=-2
        elif self.result>=0 :
            QMessageBox.information(self,"结果", "匹配成功 从母串第" + str(self.result + 1) + "位开始相同", QMessageBox.Yes)
            self.result=-2






if __name__ == '__main__':
    app = QApplication(sys.argv)
    KMP = KMP()
    app.exec_()
