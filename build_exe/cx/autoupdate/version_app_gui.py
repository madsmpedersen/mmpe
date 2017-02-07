import sys
import esky
import os
from esky import Esky
from mmpe.build_exe.cx.autoupdate import version_app_ui, autoupdate
from mmpe.QtGuiLoader.QtGuiLoader import QtMainWindowLoader
from mmpe.ui.qt_ui import QtUI
import traceback
from mmpe.ui import UI
version = (1, 1, 56)





class VersionApp(QtUI, QtMainWindowLoader):
    def __init__(self, parent=None):

        ui_module = version_app_ui
        try: self.ui = ui_module.Ui_Form()  #enable autocomplete
        except: pass
        QtMainWindowLoader.__init__(self, ui_module)
        QtUI.__init__(self, parent=self)
        self.setWindowTitle("Version %d.%d.%d" % version)
        

        print (os.path.isfile('pydap.ico'))
        ico = QIcon('pydap.ico')
        print (ico)
        self.setWindowIcon(ico)
        print (self.windowIcon())
        print (os.getcwd())
        self.version = version
        autoupdate(r"http://tools.windenergy.dtu.dk/pdap/downloads/versions.htm", self)




if __name__ == "__main__":
    try:
        os.rename(r'C:\mmpe\programming\python\MMPE\build_exe\cx\autoupdate\appdata\version_app-1.1.27.win-amd64', r'C:\mmpe\programming\python\MMPE\build_exe\cx\autoupdate\appdata\version_app-1.1.25.win-amd64')
    except:
        pass
    try:
        va = VersionApp()
        va.start()
    except Exception as e:
        if hasattr(sys.__stderr__, 'write'):
            sys.__stderr__.write(traceback.format_exc())

#    if 1 or hasattr(sys, "frozen"):
#
