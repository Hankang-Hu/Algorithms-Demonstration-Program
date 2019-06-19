# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import *

class Graduation_Projrct(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("基于Python的算法演示软件")
        self.setFixedSize(400, 150)
        self.pushButton=QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(80, 50,80 , 50))
        self.pushButton.setText('模块A')
        self.pushButton.clicked.connect(self.firstw)
        self.pushButton_2 = QPushButton(self)
        self.pushButton_2.setGeometry(QtCore.QRect(240,50,80, 50))
        self.pushButton_2.setText("模块B")
        self.pushButton_2.clicked.connect(self.secondw)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', '确定要退出吗?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:event.ignore()

    def firstw(self):
        from modle_A import MainWindow
        self.demo1 = MainWindow()
    def secondw(self):
        from modle_B import Ui_frame
        self.demo2 = Ui_frame()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = Graduation_Projrct()
    mainwindow.show()
    sys.exit(app.exec_())
