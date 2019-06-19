import sys
import time
import re
import threading
import inspect
import ctypes
import winsound
import math
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

class Hannota(QWidget):
    time = 0.05
    inputs1 = 0
    inputs2 = 0
    isend = -1
    counter=0
    def __init__(self):
        super().__init__()
        self.setWindowTitle("汉诺塔")
        self.setFixedSize(950, 700)

        self.paintarea = PaintArea(self)
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.paintarea)
        sub_layout = QHBoxLayout()
        sub_layout.setContentsMargins(10, 10, 10, 10)

        self.combobox_1 = QComboBox(self)
        self.combobox_1.addItem("手动模式")
        self.combobox_1.addItem("自动运行")
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

    def hannota(self,n, a, b, c):  #移动步骤
        if n == 1:
            self.movedisc(a,c)
        else:
            self.hannota(n - 1, a, c, b)
            self.movedisc(a, c)
            self.hannota(n - 1, b, a, c)

    def movedisc(self,source,target):   #具体移动
        self.counter+=1
        str=self.thrName[source]+' -> '+self.thrName[target]
        self.paintarea.from_to=str
        self.paintarea.countstep=self.counter
        if source==0:
            button=self.paintarea.towerA[0]
            self.paintarea.towerA.pop(0)
        elif source==1:
            button = self.paintarea.towerB[0]
            self.paintarea.towerB.pop(0)
        elif source==2:
            button = self.paintarea.towerC[0]
            self.paintarea.towerC.pop(0)
        if self.inputs2:
            self.singal2.clear()
            self.singal2.wait()

        self.up(button,self.thrposX[source] - 15 * (button + 1),len(self.thrTower[source])+1)
        self.translation(button,self.thrposX[source]- 15 * (button + 1),self.thrposX[target]- 15 * (button + 1))
        self.paintarea.down(button,self.thrposX[target] - 15 * (button + 1), 100,len(self.thrTower[target]))
        if target==0:
            self.paintarea.towerA.insert(0,button)
        elif target==1:
            self.paintarea.towerB.insert(0,button)
        elif target==2:
            self.paintarea.towerC.insert(0,button)

    def up(self,button,x,length):
        y=335-length*15
        y1=100
        i=1
        while y>=y1:
            self.singal1.wait()
            self.paintarea.list[button].move(x, y)
            time.sleep(self.time)
            self.paintarea.repaint()
            i += 2
            y = y - i
        self.paintarea.list[button].move(x, y1)

    def translation(self,button,sour,targ):
        x1=(targ-sour)/20
        x=sour
        for i in range(20):
            self.singal1.wait()
            x+=x1
            self.paintarea.list[button].move(x, 100)
            time.sleep(self.time)
            self.paintarea.repaint()

    def begin(self):
        self.isend = 0
        self.paintarea.time=self.time
        self.thrName = ['A', 'B', 'C']
        self.thrposX = [150, 460, 770]
        self.thrTower = [self.paintarea.towerA,self.paintarea.towerB,self.paintarea.towerC]
        self.hannota(self.N,0,1,2)
        self.isend = 1

    def clicked1(self):
        self.inputs1 = self.combobox_1.currentIndex()

    def clicked2(self):
        self.inputs2 = self.combobox_2.currentIndex()

    def prepare(self):
        str = self.lineEdit.text()
        an = re.search('^[1-9]\d*$', str)
        if an:
            if int(str) > 9 or int(str)<1:
                QMessageBox.information(self, "警告", "非法数值", QMessageBox.Yes)
            else:
                self.N=int(str)
                self.paintarea.N = self.N
                self.paintarea.init()
                if self.inputs1==0:
                    self.paintarea.list[0].flag = 1
                self.paintarea.repaint()
        else:
            QMessageBox.information(self, "警告", "非法格式", QMessageBox.Yes)

    def run(self):
        if self.inputs1:
            self.singal1 = threading.Event()
            if self.inputs2:
                self.singal2 = threading.Event()
            self.singal1.set()
            self.t = threading.Thread(target=self.begin)
            self.t.start()
        else:
            pass

    def pause(self):
        self.singal1.clear()
        self.paintarea.singal1.clear()

    def resume(self):
        self.singal1.set()
        self.paintarea.singal1.set()

    def steps(self):
        self.singal2.set()

    def closeEvent(self, event):
        if self.isend==0:
            stop_thread(self.t)

class Button(QPushButton):
    flag=0
    def __init__(self, parent):
        super().__init__( parent)

    def mouseMoveEvent(self, e):
        if self.flag:
            if e.buttons() != Qt.LeftButton:
                return

            mimeData = QMimeData()

            drag = QDrag(self)
            drag.setMimeData(mimeData)
            drag.setHotSpot(e.pos() - self.rect().topLeft())

            dropAcion = drag.exec_(Qt.MoveAction)

class PaintArea(QWidget):
    time = 0.05
    countstep=0
    from_to=' -> '
    def __init__(self, Parent=None):
        super().__init__(Parent)
        self.setAcceptDrops(True)
        self.N = 0
        self.setPalette(QPalette(Qt.white))  # 背景颜色
        self.setAutoFillBackground(True)  # 设置窗体自动填充背景
        self.setFixedSize(950, 550)
        self.list = []
        for i in range(9):
            self.list.append(Button(self))

    def init(self):
        self.singal1 = threading.Event()
        self.singal1.set()
        self.countstep=0
        self.towerA = []
        self.towerB = []
        self.towerC = []
        for i in range(self.N):
            self.list[i].flag = 0
            self.towerA.append(i)
            self.list[i].setText(str(i+1))
            self.list[i].setGeometry(150 - 15 * (i + 1), 335-self.N*15 + (i + 1) * 15, 30 * (i + 1)+10, 15)
            self.list[i].setStyleSheet("background: rgb(0,255,0)")

    def dragEnterEvent(self, e):
        e.accept()

    def doSth(self,button):  #删除原来的塔顶 并设置原来的第二个圆盘可以拖动
        if button in self.towerA:
            self.towerA.pop(0)
            if len(self.towerA)>0:
                self.list[self.towerA[0]].flag = 1
        elif button in self.towerB:
            self.towerB.pop(0)
            if len(self.towerB)>0:
                self.list[self.towerB[0]].flag = 1
        elif button in self.towerC:
            self.towerC.pop(0)
            if len(self.towerC)>0:
                self.list[self.towerC[0]].flag = 1
        else:
            pass

    def down(self,button,x,y,length):
        y1=335-length*15
        i=1
        while y<=y1:
            self.singal1.wait()
            self.list[button].move(x, y)
            time.sleep(self.time)
            self.repaint()
            i += 2
            y = y + i
        self.list[button].move(x, y1)
        winsound.PlaySound('sound.wav', flags=1)

    def jump(self,button,position):
        self.countstep+=1
        if len(self.towerC)>0:
            score=math.pow(2,len(self.towerC)-self.N)*100
        else :score=0
        if position.x()>=150-15 * (button + 1) and position.x()<=160+15 * (button + 1):
            self.list[button].move(150 - 15 * (button + 1),position.y())
            self.doSth(button)
            self.down(button, 150 - 15 * (button + 1), position.y(), len(self.towerA))
            self.towerA.insert(0,button)
            #self.list[self.towerA[0]].flag = 1
            if(len(self.towerA)>1):
                self.list[self.towerA[1]].flag = 0
                if(self.towerA[0]>self.towerA[1]):
                    QMessageBox.information(self, "GG", "GAME OVER!你的分数是："+str(score), QMessageBox.Yes)
                    self.init()
                    self.list[0].flag = 1
                    self.repaint()

        elif position.x()>=460-15 * (button + 1) and position.x()<=470+15 * (button + 1):
            self.list[button].move(460 - 15 * (button + 1), position.y())
            self.doSth(button)
            self.down(button, 460 - 15 * (button + 1), position.y(), len(self.towerB))
            self.towerB.insert(0, button)
            #self.list[self.towerB[0]].flag = 1
            if (len(self.towerB) > 1):
                self.list[self.towerB[1]].flag = 0
                if (self.towerB[0] > self.towerB[1]):
                    QMessageBox.information(self, "GG", "GAME OVER!你的分数是：" + str(score), QMessageBox.Yes)
                    self.init()
                    self.list[0].flag = 1
                    self.repaint()

        elif position.x()>=770-15 * (button + 1) and position.x()<=780+15 * (button + 1):
            self.list[button].move(770 - 15 * (button + 1), position.y())
            self.doSth(button)
            self.down(button, 770 - 15 * (button + 1), position.y(), len(self.towerC))
            self.towerC.insert(0, button)

            if (len(self.towerC) >1):
                self.list[self.towerC[0]].flag = 1
                self.list[self.towerC[1]].flag = 0
                if (self.towerC[0] > self.towerC[1]):
                    QMessageBox.information(self, "GG", "GAME OVER!你的分数是：" + str(score), QMessageBox.Yes)
                    self.init()
                    self.list[0].flag = 1
                    self.repaint()
                elif len(self.towerC) == self.N:
                    QMessageBox.information(self, "KO", "Congratulations! 更上一层楼", QMessageBox.Yes)
            elif len(self.towerC) == self.N:
                QMessageBox.information(self, "KO", "Congratulations! 更上一层楼", QMessageBox.Yes)
        else:
            pass

    def dropEvent(self, e):
        position = e.pos()
        for i in range(self.N):
            if self.list[i].isDown():
                self.jump(i,position)
        e.setDropAction(Qt.MoveAction)
        e.accept()

    def paintEvent(self,paintEvent):
        qp = QPainter()
        qp.begin(self)
        self.draw(qp)
        qp.end()

    def draw(self,qp):
        qp.setBrush(QColor(255, 100, 100))
        qp.drawRect(150, 150, 10, 200)
        qp.drawRect(460, 150, 10, 200)
        qp.drawRect(770, 150, 10, 200)
        qp.setPen(QPen(QColor(255, 100, 0)))
        qp.setFont(QFont('Decorative', 12))
        qp.drawText(750, 90, "步    数:")
        qp.drawText(840, 90, str(self.countstep))
        qp.drawText(750, 30, "当前动作:")
        qp.drawText(840, 30, str(self.from_to))
        qp.drawText(150, 400, "A")
        qp.drawText(460, 400, "B")
        qp.drawText(770, 400, "C")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    hannota = Hannota()
    app.exec_()