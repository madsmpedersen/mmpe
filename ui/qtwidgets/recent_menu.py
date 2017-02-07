'''
Created on 25/11/2015

@author: MMPE
'''


import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMenu, QAction, QMainWindow, QApplication

from mmpe.QtGuiLoader.QtGuiLoader import QtGuiLoader, QtGuiApplication
from mmpe.ui.qt_ui import QtUI


class RecentMenu(QMenu):
    def __init__(self, parent, fileMenu, pos):
        QMenu.__init__(self, "Recent", parent)
        fileMenu.addMenu(self)

    def add(self, name):
        pass

class RecentInMenu(object):
    def __init__(self, parent, filemenu, open_func, next_element, max=10):
        self.parent = parent
        self.filemenu = filemenu
        self.open_func = open_func
        self.next_element = next_element
        self.max = max
        self.qactions = []
        for i, recent in enumerate([r for r in self.parent.load_setting('recent_lst', "").split(";") if r], 1):
            a = QAction("%d: %s" % (i, recent), self.filemenu, triggered=(lambda r=recent : lambda :self.open_wrapper(r))())
            a.recent = recent
            self.qactions.append(a)
            self.filemenu.insertAction (self.next_element, a)
        if self.qactions:
            self.next_element = self.qactions[0]

    def open_wrapper(self, recent):
        self.add(recent)
        self.open_func(recent)

    def add(self, recent):
        remove_action = None
        for a in self.qactions:
            if a.recent == recent:
                remove_action = a
                break

        a = QAction("1: " + recent, self.filemenu, triggered=(lambda r=recent : lambda :self.open_wrapper(r))())
        a.recent = recent
        self.filemenu.insertAction (self.next_element, a)
        self.qactions.insert(0, a)
        self.next_element = a
        if remove_action:
            self.qactions.remove(remove_action)
            self.filemenu.removeAction(remove_action)

        for i, a in enumerate(self.qactions, 1):
            a.setText("%d: %s" % (i, a.recent))

        recent_lst = self.parent.load_setting('recent_lst', "").split(";")
        recent_lst.insert(0, recent)
        self.parent.save_setting('recent_lst', ";".join(recent_lst[:3]))
        if len(self.qactions) > self.max:
            a = self.qactions.pop()
            self.filemenu.removeAction(a)


class TestMainWindow(QMainWindow, QtGuiApplication, QtUI):
    def __init__(self, *args, **kwargs):
        QMainWindow.__init__(self, *args, **kwargs)
        QtGuiApplication.__init__(self, self)
        QtUI.__init__(self, self)


        self.menubar = self.menuBar()
        self.fileMenu = self.menubar.addMenu('&File')
        openAction = QAction(QIcon('open.png'), '&Open...', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open...')
        openAction.triggered.connect(self.actionOpen)
        exitAction = QAction("&Exit", self, shortcut='Ctrl+Q', statusTip='Exit', triggered=app.exit)
        self.fileMenu.addAction(openAction)
        self.fileMenu.addSeparator()
        sep = self.fileMenu.addSeparator()

        self.fileMenu.addAction(exitAction)

        self.recentInMenu = RecentInMenu(self, self.fileMenu, self.open, sep)

        self.show()

    def actionOpen(self):
        f = self.get_open_filename()
        if f == "": return
        self.recentInMenu.add(f)

    def open(self, name):
        print (name)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = TestMainWindow()
    app.exec_()
