import sys
import time
import re
import threading
import inspect
import ctypes
import winsound
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

class queens(QWidget):
    time = 0.5
    inputs2 = 0
    isend = -1
    counter=0
    counter2=0
    def __init__(self):
        super().__init__()
        self.setWindowTitle("N皇后")
        self.setFixedSize(950, 700)

        self.paintarea = PaintArea(self)
        main_layout = QHBoxLayout(self)
        main_layout.addWidget(self.paintarea)
        sub_layout = QVBoxLayout()
        sub_layout.setContentsMargins(10, 10, 10, 10)


        self.lineEdit = QLineEdit()
        self.lineEdit.setParent(self)
        self.lineEdit.returnPressed.connect(self.prepare)
        sub_layout.addWidget(self.lineEdit)

        self.lable = QLabel("速度:0")
        sub_layout.addWidget(self.lable)

        self.dial = QDial(self)
        self.dial.setNotchesVisible(True)
        self.dial.setRange(0, 100)
        self.dial.valueChanged.connect(self.speed)
        sub_layout.addWidget(self.dial)

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

    def movechess(self,state, nextX):
        self.counter += 1
        temp = list(state)
        temp.append(nextX)
        self.paintarea.datas = temp
        self.paintarea.counter = self.counter
        self.paintarea.repaint()
        winsound.PlaySound('sound.wav', flags=1)
        if self.inputs2 == 1:
            self.singal.clear()
        else:
            time.sleep(self.time)
        self.singal.wait()

    def conflict(self,state, nextX):
        nextY = len(state)
        for i in range(nextY):
            # 如果下一个皇后的位置与当前的皇后位置相邻（包括上下，左右）或在同一对角线上，则说明有冲突，需要重新摆放
            if abs(state[i] - nextX) in (0, nextY - i):
                self.movechess(state,nextX)
                return True
        self.movechess(state, nextX)
        return False

    # 采用生成器的方式来产生每一个皇后的位置，并用递归来实现下一个皇后的位置。
    def queens(self,num, state=()):
        for pos in range(num):
            if not self.conflict(state, pos):
                # 产生当前皇后的位置信息
                if len(state) == num - 1:
                    yield (pos,)
                # 否则，把当前皇后的位置信息，添加到状态列表里，并传递给下一皇后。
                else:
                    for result in self.queens(num, state + (pos,)):
                        temp = list(result)
                        temp.insert(0, pos)
                        if len(temp) == num:
                            pass
                            self.counter2+=1
                            self.paintarea.counter2 = self.counter2
                        yield (pos,) + result


    def begin(self):
        self.isend = 0
        self.paintarea.result=list(self.queens(self.N))
        self.isend = 1
        self.paintarea.flag = 1
        self.paintarea.repaint()

    def clicked2(self):
        self.inputs2 = self.combobox_2.currentIndex()

    def prepare(self):
        self.counter=0
        self.counter2=0
        self.paintarea.counter = 0
        self.paintarea.counter2 = 0
        self.paintarea.result = []
        self.paintarea.datas=[]
        self.paintarea.choice=-1
        self.paintarea.combobox.clear()
        str = self.lineEdit.text()
        an = re.search('^[1-9]\d*$', str)
        if an:
            if int(str) > 8 or int(str)<4:
                QMessageBox.information(self, "警告", "非法数值", QMessageBox.Yes)
            else:
                self.N=int(str)
                self.paintarea.N = self.N
                self.paintarea.repaint()
        else:
            QMessageBox.information(self, "警告", "非法格式", QMessageBox.Yes)

    def run(self):
        self.singal = threading.Event()
        if self.inputs2==0:
            self.singal.set()
        self.t = threading.Thread(target=self.begin)
        self.t.start()

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
    def __init__(self, Parent=None):
        self.N = 1
        self.datas = []
        self.counter = 0
        self.counter2 = 0
        self.result = []
        self.flag = 0
        self.choice = -1
        super().__init__(Parent)
        self.setPalette(QPalette(Qt.white))  # 背景颜色
        self.setAutoFillBackground(True)  # 设置窗体自动填充背景
        self.setMinimumSize(780,650)  # 背景大小
        self.combobox = QComboBox(self)
        self.combobox.move(670,190)
        self.combobox.currentIndexChanged.connect(self.clicked)
    def paintEvent(self,paintEvent):
        qp = QPainter()
        qp.begin(self)
        self.draw(qp)
        qp.end()

    def draw(self,qp):
        qp.setPen(QPen(QColor(255,150, 0)))
        qp.setFont(QFont('Decorative', 20))
        width=int(640/self.N)
        b=False
        for i in range(self.N):
            b = bool(1 - b)
            if b:
                a = True
            else:
                a = False
            for j in range(self.N):
                if a:
                    qp.setBrush(QColor(250, 250, 250))
                else:
                    qp.setBrush(QColor(100, 100, 100))
                qp.drawRect(10 + i * width,10 + j * width, width, width)
                a = bool(1 - a)
        pix=QPixmap()
        pix.load("queen.png")
        for i in range(len(self.datas)):
            qp.drawPixmap(width/3+ width*self.datas[i], width/6+width*i, width*0.5, width*0.9, pix)
        qp.drawText(650, 90, "步数:")
        qp.drawText(740, 90, str(self.counter))
        qp.drawText(650, 150, "结果:")
        qp.drawText(740, 150, str(self.counter2))
        if self.flag==1:
            for i in range(len(self.result)):
                self.combobox.addItem("结果"+str(i+1))
        self.flag = 0

    def clicked(self):
        self.choice = self.combobox.currentIndex()
        if(self.choice>=0):
            self.datas=self.result[self.choice]
            self.repaint()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    queens = queens()
    app.exec_()