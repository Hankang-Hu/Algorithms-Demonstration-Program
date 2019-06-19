# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
class Ui_frame(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("算法演示-模块B")
        self.setFixedSize(950, 700)
        palette = QPalette()
        palette.setBrush(self.backgroundRole(), QBrush(QPixmap('bg3.jpg')))
        self.setPalette(palette)
        self.pushButton = QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(150, 60, 141, 51))
        self.pushButton.setText('归并排序')
        self.pushButton.clicked.connect(self.firstw)
        self.pushButton_2 = QPushButton(self)
        self.pushButton_2.setGeometry(QtCore.QRect(150, 170, 141, 51))
        self.pushButton_2.setText("堆排序")
        self.pushButton_2.clicked.connect(self.secondw)
        self.pushButton_3 = QPushButton(self)
        self.pushButton_3.setGeometry(QtCore.QRect(150, 290, 141, 51))
        self.pushButton_3.setText("N皇后")
        self.pushButton_3.clicked.connect(self.thirdw)
        self.pushButton_4 =QPushButton(self)
        self.pushButton_4.setGeometry(QtCore.QRect(150, 400, 141, 51))
        self.pushButton_4.setText("汉诺塔")
        self.pushButton_4.clicked.connect(self.fourthw)
        self.pushButton_5 =QPushButton(self)
        self.pushButton_5.setGeometry(QtCore.QRect(150, 510, 141, 51))
        self.pushButton_5.setText("KMP算法")
        self.pushButton_5.clicked.connect(self.fifthw)
        self.lable = QLabel(self)
        self.lable.setGeometry(QtCore.QRect(500, 600, 141, 51))
        _translate = QtCore.QCoreApplication.translate
        self.lable.setText(
            _translate("frame", "<html><head/><body style='font-family:楷体'><font size='5' color='white'>——晁飞鹏</font></body></html>"))
        self.show()
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', '确定要退出吗?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:event.ignore()

    def firstw(self):
        QMessageBox.information(self, "规则",
                                "默认自动模式  选择手动模式请输入1-50个不大于50的正整数，用半角逗号间隔 自动模式 请输入一个不大于50的正整数作为随机生成数组的长度 回车完成输入",
                                QMessageBox.Yes)
        from mergeSort import Merge_Sort
        self.demo1 = Merge_Sort()

    def secondw(self):
        QMessageBox.information(self, "规则","默认自动模式  选择手动模式请输入1-15个不大于99的正整数，用半角逗号间隔 自动模式 请输入一个不大于15的正整数作为随机生成数组的长度 回车完成输入",QMessageBox.Yes)
        from heapSort import Heap_Sort
        self.demo2 = Heap_Sort()

    def thirdw(self):
        QMessageBox.information(self, "规则","请输入一个4到8的正整数 回车完成输入",QMessageBox.Yes)
        from Nqueens import queens
        self.demo3 = queens()

    def fourthw(self):
        QMessageBox.information(self, "规则","默认手动模式  请输入一个1到9的正整数 回车完成输入",QMessageBox.Yes)
        from hannota import Hannota
        self.demo4 = Hannota()

    def fifthw(self):
        QMessageBox.information(self, "规则","请输入 用半角逗号间隔的字符串 第一串最少6个字符最多20个 第二串最少一个 第二串字符数不超过第一串 回车完成输入",QMessageBox.Yes)
        from kmp import KMP
        self.demo5 = KMP()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = Ui_frame()
    sys.exit(app.exec_())
