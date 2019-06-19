from PyQt5.QtWidgets import *
import sys,time,threading
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

class Element:
    def __init__(self, window, x, y,name,val):
        self.x = x
        self.y = y
        self.val = val
        self.name=str(name)
        # self.wight=wight
        self.label = QLabel("", window)
        self.label.move(x, y)
        self.label.resize(90,90)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet(
            "color:red;border:none;background-color:rgba(255,255,255,0);border-image:url("+self.name+".png);font-size:20px;")
        self.label.hide()

    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.label.move(x,y)

    def moveTo(self,x,y):
        if (self.x - x)!=0:
            k = (self.y - y) / (self.x - x)
            step=-1
            if(self.y-y<0):
                step=1
            for i in range(self.y, y, step):
                self.set_position((i - y) / k + x, i)
                # print(node.x,":",node.y)
                time.sleep(0.01)
        else:
            step = -1
            if (self.y - y < 0):
                step = 1
            for i in range(self.y, y, step):
                self.set_position(x, i)
                # print(node.x,":",node.y)
                time.sleep(0.01)

class backpack(QWidget):
    class e:
        def __init__(self,x,y,N,v):
            self.x=x
            self.y=y
            self.name=N
            self.v=v

        def set_position(self,x,y):
            self.x=x
            self.y=y

    def __init__(self):
        super().__init__()
        # self.res = [[-1 for j in range(c + 1)] for i in range(n + 1)]
        self.w=[]
        self.v=[]
        self.c=0
        self.n=5
        self.list=[]
        self.state=False
        self.state2=False
        self.x=160
        self.init_Ui()
        self.th2=threading.Thread(target=self.redraw)
        self.th2.start()

    def init_Ui(self):
        self.resize(800, 600)
        self.setWindowTitle("backpack")
        self.label1=QLabel(self)
        self.label1.setText("物品A重量")
        self.label1.resize(60,20)
        self.t1=QLineEdit(self)
        self.t1.resize(60,20)
        self.label11=QLabel(self)
        self.label11.setText("物品A价值")
        self.label11.resize(60,20)
        self.t11=QLineEdit(self)
        self.t11.resize(60,20)

        self.label2 = QLabel(self)
        self.label2.setText("物品B重量")
        self.label2.resize(60, 20)
        self.t2 = QLineEdit(self)
        self.t2.resize(60, 20)
        self.label22 = QLabel(self)
        self.label22.setText("物品B价值")
        self.label22.resize(60, 20)
        self.t22 = QLineEdit(self)
        self.t22.resize(60, 20)

        self.label3 = QLabel(self)
        self.label3.setText("物品C重量")
        self.label3.resize(60, 20)
        self.t3 = QLineEdit(self)
        self.t3.resize(60, 20)
        self.label33 = QLabel(self)
        self.label33.setText("物品C价值")
        self.label33.resize(60, 20)
        self.t33 = QLineEdit(self)
        self.t33.resize(60, 20)

        self.label4 = QLabel(self)
        self.label4.setText("物品D重量")
        self.label4.resize(60, 20)
        self.t4 = QLineEdit(self)
        self.t4.resize(60, 20)
        self.label44 = QLabel(self)
        self.label44.setText("物品D价值")
        self.label44.resize(60, 20)
        self.t44 = QLineEdit(self)
        self.t44.resize(60, 20)

        self.label5 = QLabel(self)
        self.label5.setText("物品E重量")
        self.label5.resize(60, 20)
        self.t5 = QLineEdit(self)
        self.t5.resize(60, 20)
        self.label55 = QLabel(self)
        self.label55.setText("物品E价值")
        self.label55.resize(60, 20)
        self.t55 = QLineEdit(self)
        self.t55.resize(60, 20)

        self.label1.move(650,50)
        self.label11.move(650,80)
        self.t1.move(720,50)
        self.t11.move(720,80)

        self.label2.move(650, 140)
        self.label22.move(650, 170)
        self.t2.move(720, 140)
        self.t22.move(720, 170)

        self.label3.move(650, 220)
        self.label33.move(650, 250)
        self.t3.move(720, 220)
        self.t33.move(720, 250)

        self.label4.move(650, 300)
        self.label44.move(650, 330)
        self.t4.move(720, 300)
        self.t44.move(720, 330)

        self.label5.move(650, 380)
        self.label55.move(650, 410)
        self.t5.move(720, 380)
        self.t55.move(720, 410)

        self.label6=QLabel(self)
        self.label6.setText("背包容量")
        self.label6.resize(60,20)
        self.t6=QLineEdit(self)
        self.t6.resize(60,20)
        self.label6.move(650,460)
        self.t6.move(720,460)

        self.bt1=QPushButton("开始",self)
        self.bt1.resize(110,30)
        self.bt1.move(660,510)
        self.bt1.clicked.connect(self.start)

        self.bt1 = QPushButton("装入背包", self)
        self.bt1.resize(110, 30)
        self.bt1.move(660, 560)
        self.bt1.clicked.connect(self.push)

        # self.list.append(Element(self,100,100,"A",15))
        for i in range(5):
            self.list.append(Element(self,650/5*i+650/10-45,80,chr(i+65 ),0))
        self.show()

    def set_data(self):
        self.w = []
        self.v = []
        self.c = -1
        self.n = 5
        self.l=[0,1,2,3,4,5]
        t=[self.t1,self.t2,self.t3,self.t4,self.t5]
        tt=[self.t11,self.t22,self.t33,self.t44,self.t55]
        for i in range(5):
            if t[i].text()=="" or tt[i].text()=="":
                self.n=self.n-1
                self.l.remove(i)
            else:
                self.w.append(int(t[i].text()))
                self.v.append(int(tt[i].text()))
        if not self.t6.text()=="":
            self.c=int(self.t6.text())


    def paintEvent(self, QPaintEvent):
        qp=QPainter()
        qp.begin(self)
        self.draw(qp)
        qp.end()

    def draw(self,qp):
        if self.state==True:
            w=550/(self.c+1)
            h=500/(self.n+1)
            qp.setFont(QFont("黑体", 15))
            qp.setPen(QColor(34, 139, 34))
            qp.drawText(100,580,str("背包价值为：")+str(self.res[self.n][self.c]))
            qp.drawText(350, 580, str("背包容量为：")+str(self.c))
            for i in range(self.n+1):
                for j in range(self.c+1):
                    qp.setPen(Qt.NoPen)
                    qp.setBrush(QColor(224, 255, 255))
                    qp.drawRect(j * 550 / (self.c+1) + 51, i * 500 / (self.n+1) + 51, w-2, h-2)
                    qp.setFont(QFont("黑体", 13))
                    qp.setPen(QColor(0, 0, 0))
                    if self.res[i][j]!= -1:
                        qp.drawText(j * 550 / (self.c+1) + 50+w/2, i * 500 / (self.n+1) + 50+h/2, str(self.res[i][j]))
            qp.setFont(QFont("黑体", 15))
            qp.setPen(QColor(34, 139, 34))
            for i in range(self.n+1):
                if i!=0:
                    qp.drawText(20, i*500/(self.n+1)+50+h/2,chr(self.l[i]+64))
            qp.setFont(QFont("黑体", 15))
            qp.setPen(QColor(255, 106, 106))
            for i in range(self.c+1):
                qp.drawText(i* 550 / (self.c+1) + 50+w/2, 30, str(i))

        if self.state2==True:
            qp.setPen(Qt.NoPen)
            qp.setBrush(QColor(188, 143, 143))
            qp.drawRect(150,300, 300, 150)
            qp.setBrush(QColor(255, 215, 0))
            qp.drawRect(450, 300, 80, 150)
            qp.setFont(QFont("黑体", 15))
            qp.setPen(QColor(	205, 92, 92))
            qp.drawText(465,330,str("背 包"))
            qp.setFont(QFont("黑体", 8))
            qp.drawText(460, 370, str("背包价值:")+str(self.res[self.n][self.c]))
            qp.drawText(460, 390, str("背包重量:")+str(self.get_weight()))
            qp.drawText(460, 410, str("背包容量:")+str(self.c))

    def start(self):
        if self.t6.text()=="":
            reply = QMessageBox.information(self,
                                            "提示",
                                            "请输入背包容量",
                                            QMessageBox.Yes)
            return
        self.set_data()
        self.th1=threading.Thread(target=self.bag)
        self.th1.start()
        # print(self.w)
        # print(self.v)
        # print(self.n)
        # print(self.c)

    def redraw(self):
        while True:
            self.update()
            time.sleep(0.01)

    def get_weight(self):
        wight=0
        array=self.result()
        for i in array:
            wight=wight+self.w[i]
        return wight
    def bag(self):
        for i in self.list:
            i.label.hide()
        self.state2=False
        self.state=True
        n=self.n
        w=self.w
        v=self.v
        c=self.c
        self.res = [[-1 for j in range(c + 1)] for i in range(n + 1)]
        # print(self.res)
        for j in range(c + 1):
            self.res[0][j] = 0
        for i in range(1, n + 1):
            for j in range(1, c + 1):
                self.res[i][j] = self.res[i - 1][j]
                time.sleep(0.05)
                if j >= w[i - 1] and self.res[i][j] < self.res[i - 1][j - w[i - 1]] + v[i - 1]:
                    self.res[i][j] = self.res[i - 1][j - w[i - 1]] + v[i - 1]
                    time.sleep(0.05)
        # print(self.res)
        # self.state=False
        return


    def result(self):
        n=self.n
        c=self.c
        w=self.w
        res=self.res
        array=[]
        # print('最大价值为:', res[n][c])
        x = [False for i in range(n)]
        j = c
        for i in range(1, n + 1):
            if res[i][j] > res[i - 1][j]:
                x[i - 1] = True
                j -= w[i - 1]
        # print('选择的物品为:')
        for i in range(n):
            if x[i]:
                array.append(i)
        # print(array)
        return array


    def moveElement(self):
        for i in range(5):
            self.list[i].label.hide()
            self.list[i].set_position(650 / 5 * i + 650 / 10 - 45, 80)
        self.state=False
        self.state2=True
        self.x=160
        for i in self.list:
            i.label.show()
            # print(type(str(chr(i+65))))
        # self.list.append(Element(self, 10, 10, chr(1 + 65), 0))
        # print(self.list)
        array=self.result()
        print(array)
        for i in self.list:
            for j in array:
                if i.name==str(chr(j+65)):
                    i.moveTo(self.x,355)
                    self.x=self.x+90

    def push(self):
        self.thread1=threading.Thread(target=self.moveElement)
        self.thread1.start()

if __name__ == '__main__':
    # n = 5
    # c = 10
    # w = [2, 2, 6, 5, 4]
    # v = [6, 3, 5, 4, 6]
    # res = bag(n, c, w, v)
    # show(n, c, w, res)
    app = QApplication(sys.argv)
    ex=backpack()
    sys.exit(app.exec_())