# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui\empty.ui'
#
# Created: Tue Apr  5 08:30:01 2016
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from qtpy.QtWidgets import QMenuBar, QStatusBar, QWidget
from qtpy import QtCore


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setCentralWidget(QWidget(MainWindow))
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)



