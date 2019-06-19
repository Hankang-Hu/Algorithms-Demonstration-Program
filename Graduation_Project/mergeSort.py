import sys
import time
import re
import random
import inspect
import ctypes
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import threading

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

class Merge_Sort(QWidget):
    time=0.05
    inputs1=0
    inputs2=0
    isend=-1
    def __init__(self):
        super().__init__()
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


        self.lineEdit =QLineEdit()
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
    def moveRectangles(self,source,target):
        self.paintarea.source=source
        self.paintarea.flag1=1
        x1=source * 900 / len(self.datas)
        y1=300 - self.datas[source] * 6
        x2 = target * 900 / len(self.datas)
        temp=(x2-x1)/25
        if self.inputs2:                           #单步逻辑
            self.step_single.clear()
            self.step_single.wait()
        for i in range(25):
            self.singal.wait()
            x1 = x1 + temp
            y1 = y1 + 12
            self.paintarea.x=x1
            self.paintarea.y=y1
            self.paintarea.repaint()
            time.sleep(self.time)
        self.paintarea.flag1 = 0
        self.paintarea.datas2.append([source, target])

    def backer(self,c,low):
        y1=0
        self.paintarea.back=c
        self.paintarea.begin=low
        if self.inputs2:
            self.step_single.clear()
            self.step_single.wait()
        for i in range(25):
            self.singal.wait()
            y1 = y1+12
            self.paintarea.y=y1
            self.paintarea.repaint()
            time.sleep(self.time)

    def merge(self,a,b,low,middle,high):
        c=[]
        h = j = temp = count = 0
        self.paintarea.datas2=[]
        self.paintarea.flag2 = 1
        self.paintarea.Remove=[]
        while j < len(a) and h < len(b):
            if a[j] < b[h]:
                self.paintarea.Remove.append(low+j)
                self.moveRectangles(low+j,low+count)
                c.append(a[j])
                j += 1
            else:
                self.paintarea.Remove.append(middle+1+h)
                self.moveRectangles(middle+1+h,low+count)
                c.append(b[h])
                h += 1
            count += 1
        if j == len(a):
            for i in b[h:]:
                self.paintarea.Remove.append(middle + 1 + h+temp)
                self.moveRectangles(middle + 1 + h+temp,low+count)
                c.append(i)
                temp += 1
                count += 1
        else:
            for i in a[j:]:
                self.paintarea.Remove.append(low+j+temp)
                self.moveRectangles(low+j+temp, low + count)
                c.append(i)
                temp += 1
                count += 1
        self.paintarea.flag2 = 2
        self.backer(c,low)
        self.paintarea.flag2 = 0
        self.datas[low:high + 1] = c
        self.paintarea.Remove=[]
        self.paintarea.datas1.append([low,high])
        self.paintarea.datas = self.datas
        return c

    def merge_sort(self,low,high):
        if low < high:
            middle = int((low+high)/2)
            left=self.merge_sort(low, middle)
            right=self.merge_sort(middle+1, high)
            return self.merge(left,right,low,middle,high)
        else:
            return self.datas[low:low+1]

    def begin(self):
        self.isend=0          #结束标志
        self.merge_sort(0, len(self.datas) - 1)
        self.isend=1

    def clicked1(self):
        self.inputs1=self.combobox_1.currentIndex()

    def clicked2(self):
        self.inputs2 = self.combobox_2.currentIndex()

    def prepare(self):
        self.datas=[]
        flag=0
        self.paintarea.datas1 = []
        str=self.lineEdit.text()
        if self.inputs1 == 1:
            an = re.search('^\d+(,\d+)*$',str)
            if an:
                var = str.split(',')
                if len(var)<=50 and len(str)>=1:
                    for i in var:
                        if int(i)==0 or int(i)>50:
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
                if  int(str)>50:
                    QMessageBox.information(self, "警告", "非法数值", QMessageBox.Yes)
                else:
                    for i in range(int(str)):
                        self.datas.append(random.randint(1, 50))
            else:
                QMessageBox.information(self,"警告", "非法格式",QMessageBox.Yes)
        self.paintarea.datas = self.datas
        self.paintarea.repaint()

    def run(self):
        if self.inputs2 :
            self.step_single= threading.Event() #单步暂停信号
        self.singal = threading.Event()    #线程内置暂停信号
        self.singal.set()
        self.t = threading.Thread(target=self.begin)
        self.t.start()

    def pause(self):
        self.singal.clear()

    def resume(self):
        self.singal.set()

    def steps(self):
        self.step_single.set()

    def closeEvent(self, event):    #退出事件
        if(self.isend==0):
            stop_thread(self.t)     #线程结束
class PaintArea(QWidget):
    datas=[]
    datas1=[]
    datas2 = []
    Remove=[]
    flag1=0
    flag2=0
    def __init__(self, Parent=None):
        super().__init__(Parent)
        self.setPalette(QPalette(Qt.white))  # 背景颜色
        self.setAutoFillBackground(True)  # 设置窗体自动填充背景
        self.setMinimumSize(900, 600)  # 背景大小

    #def colors(self,i):


    def paintEvent(self,paintEvent):
        qp = QPainter()
        qp.begin(self)
        self.drawRectangles(qp)
        qp.end()

    def drawRectangles(self,qp):
        length=len(self.datas)
        for i in range(length):
            if i not in self.Remove:
                qp.setBrush(QColor(255-(255/length)*i,(127+(255/length)*i)%255,(255/length)*i))
                qp.drawRect(i*900/length, 300-self.datas[i]*6, 900/length, self.datas[i]*6)

        for i in range(len(self.datas1)):
            qp.setBrush(QColor(255 - (255 / length) * self.datas1[i][0], (127 + (255 / length) * self.datas1[i][0]) % 255,(255 / length) * self.datas1[i][0]))
            for j in range(self.datas1[i][1]-self.datas1[i][0]+1):
                k=self.datas1[i][0] + j
                if  k not in self.Remove:
                    qp.drawRect(k * 900 / length, 300 - self.datas[k] * 6, 900 / length, self.datas[k] * 6)

        if self.flag1==1:
            qp.setBrush(QColor(255-(255/length)*self.source,(127+(255/length)*self.source)%255,(255/length)*self.source))
            qp.drawRect(self.x,self.y, 900 / length, self.datas[self.source] * 6)

        if self.flag2 == 1:
            for j in range(len(self.datas2)):
                qp.setBrush(QColor(255 - (255 / length) * self.datas2[0][1], (127 + (255 / length) * self.datas2[0][1]) % 255,(255 / length) * self.datas2[0][1]))
                qp.drawRect(self.datas2 [j][1]*900/length, 600-self.datas[self.datas2[j][0]]*6, 900/length, self.datas[self.datas2[j][0]]*6)

        if self.flag2==2:
            qp.setBrush(QColor(255 - (255 / length) * self.datas2[0][1], (127 + (255 / length) * self.datas2[0][1]) % 255, (255 / length) * self.datas2[0][1]))
            for i in range(len(self.back)):
                qp.drawRect((i+self.datas2[0][1])*900/length, 600-self.y-self.back[i]*6, 900/length, self.back[i]*6)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Merge_Sort()
    app.exec_()