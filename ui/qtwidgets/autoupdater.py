

from PyQt4 import QtGui
from mmpe.QtGuiLoader.QtGuiLoader import QtGuiApplication, QtMainWindowLoader
from mmpe.ui.qt_ui import QtUI
import sys
from mmpe.build_exe.cx.autoupdate import autoupdate
from mmpe.ui.qtwidgets import main_windowUI
class AutoUpdater(object):
    def __init__(self, url):
        self.url = url



    def post_initialize(self):
        print ("here")
        if 1 or hasattr(sys, "frozen"):
            autoupdate(self.url + r"index.htm", 'HAWC2Launcher', self)





class TestMainWindow(QtMainWindowLoader, QtUI, AutoUpdater):
    def __init__(self):
        QtMainWindowLoader.__init__(self, main_windowUI)
        QtUI.__init__(self, self)
        AutoUpdater.__init__(self, url=r'http://tools.windenergy.dtu.dk/HAWC2Launcher/downloads/')


    def post_initialize(self):
        AutoUpdater.post_initialize(self)


#    def __init__(self, *args, **kwargs):
#        QtGui.QMainWindow.__init__(self, *args, **kwargs)
#
#        QtUI.__init__(self, self)
#        AutoUpdater.__init__(self, r'http://tools.windenergy.dtu.dk/HAWC2Launcher/downloads/')


#        self.menubar = self.menuBar()
#        self.fileMenu = self.menubar.addMenu('&File')
#        openAction = QtGui.QAction(QtGui.QIcon('open.png'), '&Open...', self)
#        openAction.setShortcut('Ctrl+O')
#        openAction.setStatusTip('Open...')
#        openAction.triggered.connect(self.actionOpen)
#        exitAction = QtGui.QAction("&Exit", self, shortcut='Ctrl+Q', statusTip='Exit', triggered=app.exit)
#        self.fileMenu.addAction(openAction)
#        self.fileMenu.addSeparator()
#        sep = self.fileMenu.addSeparator()
#
#        self.fileMenu.addAction(exitAction)
#
#        self.recentInMenu = RecentInMenu(self, self.fileMenu, self.open, sep)

        self.show()

#    def actionOpen(self):
#        f = self.get_open_filename()
#        if f == "": return
#        self.recentInMenu.add(f)
#
#    def open(self, name):
#        print (name)
#

if __name__ == "__main__":
    mainWindow = TestMainWindow()
    mainWindow.start()
