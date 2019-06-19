import sys,time,random,threading,re
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic.properties import QtGui


class TreeNode:
    def __init__(self, window,val, x, y):
        self.x = x
        self.y = y
        self.val = val
        self.label = QLabel(str(val), window)
        self.label.move(x, y)
        self.label.resize(60,60)
        self.label.setAlignment(Qt.AlignCenter)
        # str="color:red;border:none;background-color:rgba(255,255,255,0);border-image:url(AlgorithmDemo/element.png);font-size:20px;"
        self.label.setStyleSheet("color:red;border:none;background-color:rgba(255,255,255,0);border-image:url(element.png);font-size:20px;")
        self.label.show()
        self.left = None
        self.right = None

    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.label.move(x,y)

    def moveTo(self,x,y):
        if (self.x - x)!=0:
            k = (self.y - y) / (self.x - x)
            step=-10
            if(self.y-y<0):
                step=10
            for i in range(self.y, y, step):
                self.set_position((i - y) / k + x, i)
                # print(node.x,":",node.y)
                time.sleep(0.01)
        else:
            step = -10
            if (self.y - y < 0):
                step = 10
            for i in range(self.y, y, step):
                self.set_position(x, i)
                # print(node.x,":",node.y)
                time.sleep(0.01)

class BinarySerchTree(QWidget):

    def __init__(self):
        super().__init__()
        self.treeNodeList=[]
        self.root=None
        self.init_Ui()
        # self.t1=threading.Thread(target=self.reDraw)
        # self.t1.start()
        # self.move(self.nodeList[0], 50, 50)

    def init_Ui(self):
        self.resize(900,620)
        self.setWindowTitle("BinarySerchTree")
        self.label1=QLabel("输入数组：",self)
        self.label1.move(10,580)
        self.label1.resize(60,25)
        self.label2=QLabel("待查元素：",self)
        self.label2.move(580,580)
        self.label2.resize(60,25)
        self.textbox1 = QLineEdit(self)
        self.textbox2=QLineEdit(self)
        self.textbox1.move(70, 580)
        self.textbox1.resize(280, 25)
        self.textbox2.move(640,580)
        self.textbox2.resize(80,25)
        self.bt1=QPushButton("创建数组",self)
        self.bt1.resize(80,25)
        self.bt2=QPushButton("构造二叉树",self)
        self.bt2.resize(80, 25)
        self.bt3=QPushButton("查找元素",self)
        self.bt3.resize(80, 25)
        self.bt1.move(360, 580)
        self.bt2.move(450,580)
        self.bt3.move(730,580)
        self.bt1.clicked.connect(self.set_array)
        self.bt2.setEnabled(False)
        self.bt2.clicked.connect(self.tree)
        # palette = QPalette()
        # palette.setBrush(self.backgroundRole(), QBrush(QPixmap('AlgorithmDemo/bg5.png')))
        # # self.bt1.setWindowOpacity(0.6)
        # self.setAutoFillBackground(True)
        # self.setPalette(palette)
        self.bt3.clicked.connect(self.serchT)
        # self.setStyleSheet("background-image:url(AlgorithmDemo/bg5.png)")
        # self.widget=QWidget(self)
        # self.widget.resize(880,560)
        # self.widget.move(10,10)
        # self.widget.setStyleSheet("border-image:url(AlgorithmDemo/bg5.jpg)")
        self.show()

    def dels(self):
        for i in self.treeNodeList:
            i.label.deleteLater()
        del self.treeNodeList
        self.treeNodeList=[]
        print(self.treeNodeList)

    def init_NodeList(self,array):
        if self.root is not None:
            self.root=None
        # print(len(self.treeNodeList))
        if len(self.treeNodeList)!=0:
            self.dels()
        # print(len(self.treeNodeList))
        self.update()
        for i in range(len(array)):
            self.treeNodeList.append(TreeNode(self,array[i],int(880/len(array)*(i+0.5)-20),500))

    def insert(self,root, node,offsetx=0,offsety=0,s=1):
        if root is None:
            node.moveTo(415 + offsetx, 50 + offsety)
            self.update()
            root = node
            if self.root==None:
                self.root=root
                print("root")
            # x=340
            # y=50
            print(offsetx, ":", offsety)
        else:
            if node.val < root.val:
                root.left=self.insert(root.left, node,offsetx-180/s,offsety+70,s+1.3)
            else:
                root.right=self.insert(root.right, node,offsetx+180/s,offsety+70,s+1.3)
        return root

    def query(self,root, val):
        x=0.4
        if root is None:
            return
        if root.val is val:
            root.label.setStyleSheet(
            "color:red;border:none;background-color:rgba(255,255,255,0);border-image:url(AlgorithmDemo/this.png);font-size:20px;")
            # time.sleep(1)
            # root.label.setStyleSheet(
            #     "border:none;background-color:rgba(255,255,255,0);border-image:url(Algorithm/element.png);font-size:20px;")
            return
        if root.val < val:
            root.label.setStyleSheet(
                "color:red;border:none;background-color:rgba(255,255,255,0);border-image:url(AlgorithmDemo/this.png);font-size:20px;")
            time.sleep(x)
            root.label.setStyleSheet(
                "color:red;border:none;background-color:rgba(255,255,255,0);border-image:url(AlgorithmDemo/element.png);font-size:20px;")
            time.sleep(x)
            root.label.setStyleSheet(
                "color:red;border:none;background-color:rgba(255,255,255,0);border-image:url(AlgorithmDemo/this.png);font-size:20px;")
            time.sleep(x)
            root.label.setStyleSheet(
                "color:red;border:none;background-color:rgba(255,255,255,0);border-image:url(AlgorithmDemo/element.png);font-size:20px;")
            time.sleep(x)
            return self.query(root.right, val)
        else:
            root.label.setStyleSheet(
                "color:red;border:none;background-color:rgba(255,255,255,0);border-image:url(AlgorithmDemo/this.png);font-size:20px;")
            time.sleep(x)
            root.label.setStyleSheet(
                "color:red;border:none;background-color:rgba(255,255,255,0);border-image:url(AlgorithmDemo/element.png);font-size:20px;")
            time.sleep(x)
            root.label.setStyleSheet(
                "color:red;border:none;background-color:rgba(255,255,255,0);border-image:url(AlgorithmDemo/this.png);font-size:20px;")
            time.sleep(x)
            root.label.setStyleSheet(
                "color:red;border:none;background-color:rgba(255,255,255,0);border-image:url(AlgorithmDemo/element.png);font-size:20px;")
            time.sleep(x)
            return self.query(root.left, val)


    def getTree(self):
        self.bt2.setEnabled(False)
        for i in self.treeNodeList:
            self.insert(self.root,i)

    def tree(self):
        self.t2=threading.Thread(target=self.getTree)
        self.t2.start()

    def set_array(self):
        L=[]
        array=[]
        if self.textbox1.text()=="":
            for i in range(10):
                L.append(random.randint(1, 50))
                print(L)
        else:
            pattern = "^[\d+，]*[\d+]$"
            if (re.match(pattern, self.textbox1.text()) == None):
                reply = QMessageBox.information(self,
                                                "提示",
                                                "错误的输入",
                                                QMessageBox.Yes)
                return
            L=self.textbox1.text().split("，")
            L = list(map(int, L))
        for i in L:
            if i not in array:
                if len(array) >=10:
                    break
                array.append(i)
        print()
        self.init_NodeList(array)
        self.bt2.setEnabled(True)

    def delnum(self,root, val):
        if root is None:
            return
        if val < root.val:
            return self.delnum(root.left, val)
        elif val > root.val:
            return self.delnum(root.right, val)
        else:
            if (root.left and root.right):

                tmp = self.findmin(root.right)
                root.val = tmp.val
                root.right = self.delnum(root.right, val)
            else:
                if root.left is None:
                    root = root.right
                elif root.right is None:
                    root = root.left
        return root

    def serch(self):
        for i in self.treeNodeList:
            i.label.setStyleSheet(
                "color:red;border:none;background-color:rgba(255,255,255,0);border-image:url(AlgorithmDemo/element.png);font-size:20px;")

        e=int(self.textbox2.text())
        self.query(self.root,e)

    def serchT(self):
        self.t3 = threading.Thread(target=self.serch)
        self.t3.start()

    def paintEvent(self, QPaintEvent):
        qp=QPainter()
        qp.begin(self)
        # qp.setRenderHint(QtGui.QPainter.Antialiasing)
        self.draw(qp)
        # print("ssss")
        qp.end()

    def draw(self, qp):
        qp.setRenderHint(QPainter.Antialiasing)
        qp.setPen(Qt.NoPen)
        qp.drawPixmap(10,10,880,560,QPixmap('bg5.jpg'))
        pen=QPen()
        pen.setWidth(2)
        # pen.setCapStyle(Qt.RoundCap)
        pen.setColor(QColor(255,255,255))
        qp.setPen(pen)
        # print(N)
        for i in self.treeNodeList:
            if i.left!=None:
                qp.drawLine(i.x+30,i.y+60,i.left.x+30,i.left.y)
            if i.right!=None:
                qp.drawLine(i.x+30, i.y+60, i.right.x+30, i.right.y)


if __name__=="__main__":
    app=QApplication(sys.argv)
    a=BinarySerchTree()
    # time.sleep(2)
    # t1 = threading.Thread(target=a.moveNode,args=(a.nodeList[0],50,50))
    # t1 = threading.Thread(target=a.getTree)
    # t2 = threading.Thread(target=a.reDraw)
    # t2.start()
    # t1.start()
    sys.exit(app.exec_())