import sys,time,threading
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt


class point:
    def __init__(self,x,y):
        self.x=x
        self.y=y

    def __eq__(self, other):
        if self.x==other.x and self.y==other.y:
            return True
        return False

class Astar(QWidget):

    class Node: #节点数据类型
        def __init__(self,Point,endPoint,g=0):
            self.point=Point
            self.father=None
            self.g=g
            self.h=(abs(endPoint.x-Point.x)+abs(endPoint.y-Point.y))*10

    def __init__(self):
        super().__init__()
        self.n=0
        self.m=0
        self.speed1=0.0001
        self.speed2=0.05
        # self.set_Map(10)
        # self.array=[[0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        # self.array=[[0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 1, 0, 0, 0, 0], [0, 0, 1, 0, 0, 1, 1, 1, 0, 0], [0, 0, 0, 0, 1, 1, 0, 0, 0, 0], [1, 1, 1, 1, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 1, 0, 0], [0, 0, 1, 1, 1, 1, 0, 1, 0, 0], [0, 0, 1, 0, 0, 0, 0, 1, 0, 0], [0, 0, 1, 1, 1, 1, 0, 1, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        self.passTag=0
        self.t2 = threading.Thread(target=self.redraw)
        self.t2.start()
        self.init_Ui()



    # 获取openlist中f值最小的节点
    def get_minNode(self):
        currentNode=self.openList[0]
        for i in self.openList:
            if i.g+i.h<currentNode.g+currentNode.h:
                currentNode=i
        return currentNode

    # 判断该点是否在closelist中
    def pointInCloseist(self,point):
        for i in self.closeList:
            if i.point.__eq__(point):
                return i
        return None

    # 判断该点是否在openlist中
    def pointInOpenlist(self,point):
        for i in self.openList:
            if i.point.__eq__(point):
                return i
        return None

    def endPointInCloselist(self):
        for i in self.closeList:
            if i.point.__eq__(self.endPoint):
                return i
        return None

    #搜索周围节点
    def searchNear(self,minNode,offsetX,offsetY):
        if minNode.point.x+offsetX<0 or minNode.point.x+offsetX>self.n-1 or minNode.point.y+offsetY<0 or minNode.point.y+offsetY>self.n-1:
            return
        if self.array[minNode.point.x+offsetX][minNode.point.y+offsetY]!=self.passTag:
            return
        currentPoint =point(minNode.point.x+offsetX,minNode.point.y+offsetY)
        if self.pointInOpenlist(currentPoint):
            return
        if offsetX==0 or offsetY==0:
            step=10
        else:
            step=14
        currentNode=self.pointInOpenlist(currentPoint)
        if not currentNode:
            currentNode=Astar.Node(currentPoint, self.endPoint, g=minNode.g+step)
            currentNode.father=minNode
            self.openList.append(currentNode)
            time.sleep(self.speed1)
            return
        if minNode.g+step<currentNode:
            currentNode.g=minNode.g+step
            currentNode.father=minNode

    def getPath(self):
        if self.array[self.endPoint.x][self.endPoint.y]!=self.passTag:
            return None
        startNode=Astar.Node(self.startPoint,self.endPoint)
        self.openList.append(startNode)
        while True:
            minNode=self.get_minNode()
            self.closeList.append(minNode)
            self.openList.remove(minNode)
            self.searchNear(minNode,-1,0)
            for i in self.closeList:
                print(i.point.x,"  ",i.point.y)
            print("##########")
            self.searchNear(minNode, 0, 1)
            self.searchNear(minNode, 1, 0)
            self.searchNear(minNode, 0, -1)
            Node =self.endPointInCloselist()
            if Node:
                endNode = Node
                while True:
                    if endNode.father:
                        endNode = endNode.father
                        self.array[endNode.point.x][endNode.point.y]=2
                        time.sleep(self.speed2)
                    else:
                        return
            if len(self.openList) == 0:
                return

    def redraw(self):
        while True:
            self.update()
            # print("sss")
            time.sleep(0.01)

    def set_Map(self,n): #初始化地图
        # self.n=n
        if n==0:
            self.array=[]
        else:
            self.array=[[0 for i in range(n)] for i in range(n)]
        print(self.array)

    # def set_startPoint(self,startPoint): #设置起点
    #     if isinstance(startPoint,point):
    #         self.startPoint=startPoint
    #     else:
    #         self.startPoint=point(*startPoint)
    #
    # def set_endPoint(self,endPoint): #设置终点
    #     if isinstance(endPoint,point):
    #         self.endPoint=endPoint
    #     else:
    #         self.endPoint=point(*endPoint)

    def init_Ui(self): #初始化窗口
        w=690
        h=600
        self.resize(w,h)
        self.setWindowTitle("Map")
        self.rbt1=QRadioButton("10 * 10",self)
        self.rbt2 = QRadioButton("15 * 15", self)
        self.rbt3 = QRadioButton("20 * 20", self)
        self.bt1 = QPushButton("开始", self)
        self.rbt1.move(590,70)
        self.rbt2.move(590,120)
        self.rbt3.move(590,170)
        self.rbtg=QButtonGroup(self)
        self.rbtg.addButton(self.rbt1,10)
        self.rbtg.addButton(self.rbt2,15)
        self.rbtg.addButton(self.rbt3,20)
        self.rbtg.buttonClicked.connect(self.init_Map)
        self.bt1.clicked.connect(self.runn)
        self.bt2=QPushButton("重置地图",self)
        self.bt3 = QPushButton("设置起点", self)
        self.bt4 = QPushButton("设置终点", self)
        self.bt5 = QPushButton("确定", self)
        self.bt6 = QPushButton("终止", self)
        self.bt2.move(590, 290)
        self.bt1.move(590, 340)
        self.bt3.move(590, 390)
        self.bt4.move(590, 440)
        self.bt5.move(590, 490)
        self.bt6.move(590, 540)
        self.bt2.clicked.connect(self.reset_Map)
        self.bt3.clicked.connect(self.setstart)
        self.bt4.clicked.connect(self.setend)
        self.bt5.clicked.connect(self.set)
        self.bt6.clicked.connect(self.end)
        self.show()

    def init_Map(self):
        if self.rbtg.checkedId()==10:
            self.m=10
        elif self.rbtg.checkedId()==15:
            self.m=15
        elif self.rbtg.checkedId()==20:
            self.m=20
        self.openList = []
        self.closeList = []
        if self.m==10:
            self.n=10
            self.set_Map(10)
            self.startPoint = point(0, 0)
            self.endPoint = point(5, 0)
            self.array = [[0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
                          [0, 0, 1, 0, 0, 1, 1, 1, 0, 0], [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
                          [1, 1, 1, 1, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 1, 0, 0],
                          [0, 0, 1, 1, 1, 1, 0, 1, 0, 0], [0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
                          [0, 0, 1, 1, 1, 1, 0, 1, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        elif self.m==15:
            self.n=15
            self.set_Map(15)
            self.startPoint = point(0, 10)
            self.endPoint = point(7, 6)
            self.array=[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        elif self.m==20:
            self.n=20
            self.set_Map(20)
            self.startPoint = point(0, 0)
            self.endPoint = point(19, 2)
            self.array=[[0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0], [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
            print("aaaa")
        print(self.n)

    def paintEvent(self, QPaintEvent):
        qp=QPainter()
        qp.begin(self)
        self.draw_Map(qp)
        # print("ssss")
        qp.end()

    def draw_Map(self,qp): #绘制迷宫
        qp.setPen(Qt.NoPen)
        qp.setBrush(QColor(205, 205, 180))
        qp.drawRect(580, 20, 95, 220)
        qp.drawRect(580, 250, 95, 325)
        N=self.n
        if N==0:
            return
        if N==10:
            textSize=10
            bt=15
        elif N==15:
            textSize=6
            bt=10
        else:
            textSize=0
            bt=0
        w=500/N-2
        h=w
        for i in range(N):
            for j in range(N):
                qp.setPen(Qt.NoPen)
                qp.setBrush(QColor(220, 220, 220))
                # print(111)
                if self.array[i][j]==1:
                    qp.setBrush(QColor(131, 139, 131))
                if self.startPoint.__eq__(point(i,j)):
                    qp.setBrush(QColor(255, 0, 0))
                elif self.array[i][j]==2:
                    qp.setBrush(QColor(238, 169, 184))
                elif self.endPoint.__eq__(point(i,j)):
                    qp.setBrush(QColor(72, 118, 255))
                elif self.pointInCloseist(point(i,j)):
                    qp.setBrush(QColor(159, 182, 205))
                elif self.pointInOpenlist(point(i,j)):
                    qp.setBrush(QColor(255, 215, 0))

                qp.drawRect(j*560/N+21,i*560/N+21,w,h)
                qp.setFont(QFont("宋体", textSize))
                qp.setPen(QColor(0, 0, 0))
                node = None
                p = point(i, j)
                if self.pointInOpenlist(p):
                    node = self.pointInOpenlist(p)
                elif self.pointInCloseist(p):
                    node = self.pointInCloseist(p)
                if node and N!=20:
                    qp.drawText(j * 560 / N + 23, i * 560 / N + 30, str("G=" + str(node.g)))
                    qp.drawText(j * 560 / N + 23, i * 560 / N + 30+bt, str("H=" + str(node.h)))
                    qp.drawText(j * 560 / N + 23, i * 560 / N + 30+2*bt, str("F=" + str(node.g + node.h)))

    def runn(self):
        if self.m==0 or self.startPoint.__eq__(point(-1,-1)) or self.endPoint.__eq__(point(-1,-1)):
            reply = QMessageBox.information(self,
                                            "提示",
                                            "没有设置起点或终点",
                                            QMessageBox.Yes)
            return
        self.remap()
        self.t1 = threading.Thread(target=self.getPath)
        self.t1.start()

    def reset_Map(self):
        self.remap()
        if self.m==0:
            reply = QMessageBox.information(self,
                                            "提示",
                                            "请选择地图规模",
                                            QMessageBox.Yes)
            return
        self.set_Map(self.m)
        self.startPoint = point(-1,-1)
        self.endPoint = point(-1,-1)
        if self.setstart==True:
            self.setstart=False
            self.bt3.setEnabled(True)
        if self.setend==True:
            self.setend=False
            self.bt4.setEnabled(True)
        self.setmap=True

    def setstart(self):
        if self.m==0:
            reply = QMessageBox.information(self,
                                            "提示",
                                            "请选择地图规模",
                                            QMessageBox.Yes)
            return
        self.setstart=True
        self.bt3.setEnabled(False)
        if self.setmap==True:
            self.setmap=False
            self.bt2.setEnabled(True)
        if self.setend==True:
            self.setend=False
            self.bt4.setEnabled(True)

    def setend(self):
        if self.m==0:
            reply = QMessageBox.information(self,
                                            "提示",
                                            "请选择地图规模",
                                            QMessageBox.Yes)

        self.setend=True
        self.bt4.setEnabled(False)
        if self.setstart==True:
            self.setstart=False
            self.bt3.setEnabled(True)
        if self.setmap==True:
            self.setmap=False
            self.bt2.setEnabled(True)

    def set(self):
        if self.setmap==True:
            self.bt2.setEnabled(True)
            self.setmap=False
        if self.setstart==True:
            self.bt3.setEnabled(True)
            self.setstart=False
        if self.setend==True:
            self.bt4.setEnabled(True)
            self.setend = False

    def mousePressEvent(self, QMouseEvent):
        s=QMouseEvent.button()
        x=QMouseEvent.x()
        y=QMouseEvent.y()
        # print("鼠标按下了:",x,"+",y)
        if x>21 and x<581 and y>21 and y<581 and self.m!=0:
            array_x = int((x - 21) / (560 / self.n))
            array_y = int((y - 21) / (560 / self.n))
            if self.setmap==True:
                if s==1:
                    self.array[array_y][array_x]=1
                if s==2:
                    self.array[array_y][array_x] = 0
            elif self.setstart==True:
                if s==1:
                    self.startPoint=point(array_y,array_x)
            elif self.setend==True:
                if s==1:
                    self.endPoint=point(array_y,array_x)
        # print(self.array)
        # self.update()

    def remap(self):
        self.openList=[]
        self.closeList=[]
        for i in range(self.n):
            for j in range(self.n):
                if self.array[i][j]==2:
                    self.array[i][j]=0

    def end(self):
        self.speed1=0
        self.speed2=0
        time.sleep(1)
        self.speed1=0.0001
        self.speed2=0.05

if __name__=="__main__":
    app=QApplication(sys.argv)
    a=Astar()
    # t1 = threading.Thread(target=a.getPath)
    # t2 = threading.Thread(target=a.redraw)
    # t1.start()
    # t2.start()
    sys.exit(app.exec_())