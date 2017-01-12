'''
Created on 21/05/2013

@author: Mads M. Pedersen (mmpe@dtu.dk)
'''
import sys

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import pyqtSignal
from mmpe.functions.Decorators import postpone_until_last_call_finishes
import numpy as np


#try: range = range; range = None
#except NameError: pass
#try: str = unicode; unicode = None
#except NameError: pass
class SliderSpinBox(QtGui.QWidget):
    valueChanged = pyqtSignal(float)

    def __init__(self, parent=None, value_range=(0, 100), slider_steps=100, spinbox_steps=1000, decimals=None):
        QtGui.QWidget.__init__(self, parent)
        layout = QtGui.QHBoxLayout(self)
        self.setLayout(layout)
        self.horizontalSlider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.doubleSpinBox = QtGui.QDoubleSpinBox(self)
        self.decimals = decimals
        layout.setMargin(0)
        layout.addWidget(self.doubleSpinBox)
        layout.addWidget(self.horizontalSlider)

        self.doubleSpinBox.valueChanged.connect(self.spinbox_changed)
        self.horizontalSlider.valueChanged.connect(self.slider_changed)

        self.wt = []
        self.changer = None
        self.slider_steps = slider_steps
        self.horizontalSlider.setMaximum(slider_steps)
        self.spinbox_steps = spinbox_steps
        self.set_range(value_range)

    def set_value(self, value):
        self.doubleSpinBox.setValue(value)

    value = property(lambda self: self.doubleSpinBox.value(), set_value)

    def set_range(self, value_range):
        self.changer = "set_range"
        spinbox_step_decimal = np.ceil(np.log10(1. / (float(value_range[1] - value_range[0]) / self.spinbox_steps)))
        self.slider_decimals = int(np.ceil(np.log10(self.slider_steps) - np.log10(value_range[1] - value_range[0])))
        if self.decimals is None:
            self.doubleSpinBox.setDecimals(spinbox_step_decimal + 1)
        else:
            self.doubleSpinBox.setDecimals(self.decimals)
            spinbox_step_decimal = min(self.decimals, spinbox_step_decimal)
            self.slider_decimals = min(self.decimals, self.slider_decimals)
        self.doubleSpinBox.setSingleStep(10 ** -spinbox_step_decimal)


        self.value_range = value_range
        self.doubleSpinBox.setMinimum(value_range[0])
        self.doubleSpinBox.setMaximum(value_range[1])

        self.horizontalSlider.setValue(np.floor(value_range[0]))
        self.changer = None
        self.doubleSpinBox.setValue(value_range[0])

    def range(self):
        return self.doubleSpinBox.minimum(), self.doubleSpinBox.maximum()

    def slider_changed(self, value):
        if self.changer is None:
            self.changer = 'slider'
            value = np.round(value * (self.value_range[1] - self.value_range[0]) / self.slider_steps + self.value_range[0], self.slider_decimals)

            self.doubleSpinBox.setValue(value)
            self.changer = None
            self.value_changed(value)

    def spinbox_changed(self, value):
        if self.changer is None:
            self.changer = 'spinbox'

            slider_value = .5 + (value - self.value_range[0]) * self.slider_steps / (self.value_range[1] - self.value_range[0])
            self.horizontalSlider.setValue(slider_value)
            self.changer = None
            self.value_changed(value)

    @postpone_until_last_call_finishes
    def value_changed(self, value):
        self.valueChanged.emit(value)


class LogaritmicSliderSpinBox(SliderSpinBox):

    def __init__(self, parent=None, value_range=(0.0001, 100), slider_steps=100):
        SliderSpinBox.__init__(self, parent=parent, value_range=value_range, slider_steps=slider_steps, spinbox_steps=value_range[1] / value_range[0])

    def slider_changed(self, value):
        if self.changer is None:
            self.changer = 'slider'
            _min, _max = np.log10(self.value_range[0]), np.log10(self.value_range[1])
            value = 10 ** (_min + (float(value) * (_max - _min) / self.slider_steps))

            self.doubleSpinBox.setValue(value)
            self.changer = None
            self.value_changed(value)

    def spinbox_changed(self, value):
        if self.changer is None:
            self.changer = 'spinbox'

            _min, _max = np.log10(self.value_range[0]), np.log10(self.value_range[1])
            slider_value = (np.log10(value) - _min) * self.slider_steps / (_max - _min)
            self.horizontalSlider.setValue(slider_value)
            self.changer = None
            self.value_changed(value)


class PolynomialSliderSpinBox(SliderSpinBox):

    def __init__(self, parent=None, order=2, value_range=(0, 1000), slider_steps=100, spinbox_steps=1000):
        SliderSpinBox.__init__(self, parent=parent, value_range=value_range, slider_steps=slider_steps, spinbox_steps=spinbox_steps)
        self.coef = [(value_range[1] - value_range[0]) / slider_steps ** order, value_range[0]]
        self.order = order

    def slider_changed(self, value):
        if self.changer is None:
            self.changer = 'slider'
            _min, _max = np.log10(self.value_range[0]), np.log10(self.value_range[1])

            value = self.coef[0] * value ** self.order + self.coef[1]
            #value = 10 ** (_min + (float(value) * (_max - _min) / self.slider_steps))

            self.doubleSpinBox.setValue(value)
            self.changer = None
            self.value_changed(value)

    def spinbox_changed(self, value):
        if self.changer is None:
            self.changer = 'spinbox'

            _min, _max = np.log10(self.value_range[0]), np.log10(self.value_range[1])


            slider_value = int(((value - self.coef[1]) / self.coef[0]) ** (1 / self.order))
            self.horizontalSlider.setValue(slider_value)
            self.changer = None
            self.value_changed(value)


#class TestIt(LogaritmicSliderSpinBox):
#
#    def do_it(self, value):
#        for wt in self.wt:
#            if wt.isFinished():
#                self.wt.remove(wt)
#        wt = WorkThread(self, value)
#        wt.start()
#        self.wt.append(wt)
#
#
#class WorkThread(QtCore.QThread):
#    done = QtCore.pyqtSignal(float)
#
#    def __init__(self, holdIt, value):
#        QtCore.QThread.__init__(self)
#        self.holdIt = holdIt
#        self.value = value
#
#    def run(self):
#        t = time.time()
#        time.sleep(2)
#        self.holdIt.update_duration = time.time() - t
#        print "update finished", self.value

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    m = QtGui.QMainWindow()

    w = QtGui.QWidget()
    m.setCentralWidget(w)
    vlayout = QtGui.QVBoxLayout(w)
    s_log = LogaritmicSliderSpinBox(m, slider_steps=100)
    s_lin = SliderSpinBox(m, slider_steps=100)
    s_pol = PolynomialSliderSpinBox(m, 2, slider_steps=100, spinbox_steps=1000)
    vlayout.addWidget(s_lin)
    vlayout.addWidget(s_log)
    vlayout.addWidget(s_pol)
    #m.setCentralWidget(s)

    s_log.set_range((0.001, 1000))
    m.show()
    sys.exit(app.exec_())
