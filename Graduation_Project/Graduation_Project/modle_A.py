from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys,threading,time
from Astar import Astar
from backpack import backpack
from bubbleSort import BubbleSort
from quickSort import QuickSort
from binarySerchTree import BinarySerchTree

class MainWindow(QWidget):
    f1=None
    def __init__(self):
        super().__init__()
        self.init_UI()
        self.th()

    def init_UI(self):
        self.setWindowTitle("主界面")
        self.resize(900,650)
        self.bt1=QPushButton("冒泡排序",self)
        self.bt2 = QPushButton("快速排序", self)
        self.bt3 = QPushButton("A*算法", self)
        self.bt4 = QPushButton("0-1背包", self)
        self.bt5 = QPushButton("二叉查找树", self)
        self.bt1.resize(280,40)
        self.bt1.move(-280,100)
        self.bt2.resize(280, 40)
        self.bt2.move(-280, 200)
        self.bt3.resize(280, 40)
        self.bt3.move(-280,300)
        self.bt4.resize(280, 40)
        self.bt4.move(-280, 400)
        self.bt5.resize(280, 40)
        self.bt5.move(-280, 500)
        self.btarray=[self.bt1,self.bt2,self.bt3,self.bt4,self.bt5]
        self.setStyleSheet(
            'QPushButton{border-radius:5px;border:none;background-color:rgba(240,248,255,0);border-image:url(bt2.png);}'
            "QPushButton:hover{border-image:url(bt1.png)}"
            "QPushButton:pressed{border-image:url(bt3.png)}"
        )
        # self.bt1.setFlat(True)
        palette=QPalette()
        palette.setBrush(self.backgroundRole(),QBrush(QPixmap('bg3.jpg')))
        # self.bt1.setWindowOpacity(0.6)
        self.setAutoFillBackground(True)
        self.setPalette(palette)
        # self.lab1=QLabel("",self)
        # self.lab1.resize(150,150)
        # self.lab1.move(250,-150)
        # self.lab1.setStyleSheet("border:none;background-color:rgba(255,255,255,0);border-image:url(xixi.png)")
        self.bt1.clicked.connect(self.openBubbleSort)
        self.bt2.clicked.connect(self.openQuickSort)
        self.bt3.clicked.connect(self.openAstar)
        self.bt4.clicked.connect(self.openBackpack)
        self.bt5.clicked.connect(self.openBinaryTree)
        self.show()

    def movebt(self):
        y=100
        time.sleep(0.02)
        for i in self.btarray:
            v=10
            x=-280
            while(x<640):
                x=x+v
                i.move(x,y)
                time.sleep(0.001)
            y=y+100


    def th(self):
        self.t1=threading.Thread(target=self.movebt)
        self.t1.start()

    def openBubbleSort(self):
        if self.f1!=None:
            self.f1.close()
        self.f1=BubbleSort()
    def openQuickSort(self):
        if self.f1!=None:
            self.f1.close()
        self.f1=QuickSort()
    def openAstar(self):
        if self.f1!=None:
            self.f1.close()
        self.f1=Astar()
    def openBackpack(self):
        if self.f1!=None:
            self.f1.close()
        self.f1=backpack()
    def openBinaryTree(self):
        if self.f1!=None:
            self.f1.close()
        self.f1=BinarySerchTree()

if __name__=="__main__":
    ap=QApplication(sys.argv)
    a=MainWindow()
    #a.show()
    sys.exit(ap.exec_())
