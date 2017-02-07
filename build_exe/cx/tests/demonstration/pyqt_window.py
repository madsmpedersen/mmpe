import os


from numpy import *

from mmpe.build_exe.cx.tests.demonstration import PlotUI
from mmpe.QtGuiLoader import QtMainWindowLoader
from mmpe.ui.qtwidgets.matplotlibwidget import MatplotlibWidget


os.environ['QT_API'] = "pyqt"

#from scipy.stats import stats
class Plot(QtMainWindowLoader):
    def __init__(self):
        QtMainWindowLoader.__init__(self, PlotUI)
        self.mpl = MatplotlibWidget()
        self.ui.mplcontainer.addWidget(self.mpl)
        self.setWindowIcon(QIcon('Pydap.ico'))
        self.setWindowTitle("Test")
        self.ui.labelimage.setPixmap(QPixmap('DTU_logo.png'))
        #globals()['test'] = None

    def actionUpdate(self):

        x = arange(-pi, pi, pi / 10)
        if str(self.ui.lineEdit.text()) != "":
            y = eval(str(self.ui.lineEdit.text()));
            self.mpl.axes.plot(x, y, '--rx', linewidth=2);
            self.mpl.axes.set_title('Sine Function');
            self.mpl.draw()
            #print (stats.mode([1, 2, 3, 3, 4, 5]))

if __name__ == "__main__":
    p = Plot()
    p.start()
    #p.terminate()
    import sys
    sys.exit()
