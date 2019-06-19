import sys,time,random,re,math
import threading
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class BubbleSort(QWidget):

    array=[]
    tag=[-1,-1]
    pause=False
    state=True
    steps=False
    time = 0.25
    time2=0.01
    class element:
        def __init__(self,val,x,y):
            self.val=val
            self.x=x
            self.y=y

    def __init__(self):
        super().__init__()
        self.initUI()

    # i * (800 / num) + 52, 550 - array[i] * 10, 800 / num - 4, array[i] * 10

    def initArray(self):
        L=[]
        if self.textbox.text() == "":
            for i in range(50):
                n=random.randint(1, 50)
                self.array.append(self.element(n,i*(800/50)+52,550-n*10))
            print(self.array.__len__())
        else:
            pattern = "^[\d+，]*[\d+]$"
            if(re.match(pattern,self.textbox.text())==None):
                reply = QMessageBox.information(self,
                                                "提示",
                                                "错误的输入",
                                                QMessageBox.Yes)
                return
            L = self.textbox.text().split( "，")
            L= list(map(int, L))
            j=0
            array=[]
            for i in L:
                if j>=50:
                    break
                if i>50:
                    array.append(50)
                else:
                    array.append(i)
                j+=1
            count=array.__len__()
            for i in range(count):
                self.array.append(self.element(array[i], i * (800 / count) + 52, 540 - array[i] * 10))
        # for i in self.array:
        #     print(i.val)
        print("ok")
    def initUI(self):
        self.resize(900,620)
        self.setWindowTitle("BubbleSort")
        # self.Signal1=pyqtSignal()
        self.textbox = QLineEdit(self)
        self.textbox.move(50, 570)
        self.textbox.resize(300, 25)
        self.lab1=QLabel("输入：",self)
        self.lab1.move(15,570)
        self.lab1.resize(30,25)
        self.bt1=QPushButton("开始",self)
        self.bt2 = QPushButton("暂停", self)
        self.bt3 = QPushButton("继续", self)
        self.bt4 = QPushButton("单步", self)
        self.bt5 = QPushButton("返回", self)
        self.bt1.move(360,570)
        self.bt2.move(440,570)
        self.bt3.move(520, 570)
        self.bt4.move(600, 570)
        self.bt5.move(680, 570)
        self.bt1.clicked.connect(self.run)
        self.bt2.clicked.connect(self.Pause)
        self.bt3.clicked.connect(self.regain)
        self.bt4.clicked.connect(self.step)
        self.bt5.clicked.connect(self.close)
        # self.run()
        self.dial = QDial(self)
        self.dial.resize(60,60)
        self.dial.move(760,550)
        self.dial.setRange(0,100)
        self.dial.setNotchesVisible(True)
        self.dial.valueChanged.connect(self.speed)
        self.lab2=QLabel("速度：0",self)
        self.lab2.move(830,575)
        self.lab2.resize(70,20)
        self.show()

    def speed(self):
        self.lab2.setText("速度：" + str(self.dial.value()))
        self.time = 0.5 - 0.5 / 100 * self.dial.value()
        if self.dial.value() <= 85:
            self.time2 = 0.01 - 0.01 * (math.sin(3.14159 / 2) / 100) * (self.dial.value() + 15)
        else:
            self.time2 = 0

    def paintEvent(self,e):
        qp = QPainter()
        qp.begin(self)
        self.drawRectangles(qp)
        print("sssssss")
        qp.end()

    def drawRectangles(self, qp):
        array=self.array
        num=len(array)
        # col = QColor(0, 0, 0)
        # col.setNamedColor("#99CCFF")
        qp.setPen(Qt.NoPen)
        for i in range(num):
            if(i==self.tag[0] or i==self.tag[1]):
                qp.setBrush(QColor(255 ,106, 106))
            else:
                qp.setBrush(QColor(	0, 139, 139))
            qp.drawRect(array[i].x, array[i].y, 800/num-4, array[i].val*10)
        qp.setFont(QFont("SimSun", 10))
        qp.setPen(QColor(256, 256, 256))
        for i in range(num):
            qp.drawText(array[i].x, array[i].y-5, str(array[i].val))

    def sort(self):
        self.bt1.setEnabled(False)
        lenth=len(self.array)
        for i in range(lenth-1, 0, -1):
            for j in range(i):
                while self.pause:
                    if self.steps==True:
                        break
                    time.sleep(0.01)
                if self.array[j].val > self.array[j + 1].val:
                    self.tag[0] = j
                    self.tag[1] = j+1
                    time.sleep(self.time)
                    self.change(self.array[j],self.array[j+1])
                    num = self.array[j]
                    self.array[j] = self.array[j + 1]
                    self.array[j + 1] = num
                    # print("...")
                else:
                    self.tag[0]=j
                    self.tag[1]=j+1
                time.sleep(self.time)
                self.steps=False
        self.state=False
        self.tag=[-1,-1]
        self.bt1.setEnabled(True)

    def change(self,a,b):
        for i in range(20):
            a.y-=1
            b.y+=1
            time.sleep(self.time2)
        B=b.x
        while(a.x<B):
            a.x+=1
            b.x-=1
            time.sleep(self.time2)
        for i in range(20):
            a.y+=1
            b.y-=1
            time.sleep(self.time2)

    def repa(self):
        while self.state:
            # print(self.array)
            time.sleep(0.001)
            self.update()

    def run(self):
        self.array=[]
        self.state=True
        self.initArray()
        self.t1 = threading.Thread(target=self.sort)
        self.t2 = threading.Thread(target=self.repa)
        self.t1.start()
        self.t2.start()

    def Pause(self):
        self.pause=True

    def regain(self):
        self.pause=False
        self.time=0.005

    def step(self):
        self.pause=True
        self.steps=True

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex=BubbleSort()
    # ex.redraw()
    sys.exit(app.exec_())
