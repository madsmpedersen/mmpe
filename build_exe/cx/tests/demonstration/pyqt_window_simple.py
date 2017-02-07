import os



import sys
if hasattr(sys, "frozen"):
    os.chdir(os.path.dirname(sys.executable))
else:
    os.chdir(os.path.realpath(os.path.dirname(__file__.replace("library.zip", ""))))

for p in ["../../../../"]:
    print (os.path.realpath(p))
    if p not in sys.path:
        print ("Append" + p)
        sys.path.append(p)
from mmpe.QtGuiLoader import QtMainWindowLoader
from mmpe.build_exe.cx.tests.demonstration import PlotUI
from mmpe.build_exe import exe_std_out


os.environ['QT_API'] = "pyqt"

#from scipy.stats import stats
class Plot(QtMainWindowLoader):
    def __init__(self):
        QtMainWindowLoader.__init__(self, PlotUI)
        self.setWindowIcon(QIcon('Pydap.ico'))
        self.setWindowTitle(os.getcwd())


    def actionUpdate(self):
        pass




if __name__ == "__main__":
    p = Plot()
    p.start()
    #p.terminate()
    sys.exit()
