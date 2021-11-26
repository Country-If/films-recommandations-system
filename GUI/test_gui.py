#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = "Maylon"

from PySide2.QtWidgets import QApplication
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
from PySide2.QtGui import QIcon
import sys
import rc1
# from PySide2.QtWidgets import QPushButton, QLineEdit, QLabel, QToolButton


class Window:
    def __init__(self):
        qfile = QFile("register.ui")
        qfile.open(QFile.ReadOnly)
        qfile.close()

        self.ui = QUiLoader().load(qfile)


app = QApplication(sys.argv)
app.setWindowIcon(QIcon('dou.png'))
window = Window()
window.ui.show()
app.exec_()
