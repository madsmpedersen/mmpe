'''
Created on 13/02/2014

@author: mmpe
'''
import inspect
from types import FunctionType, MethodType
import unittest

from qtpy.QtWidgets import QApplication

from mmpe.ui.daemon_ui import DaemonUI
from mmpe.ui.qt_ui import QtOutputUI, QtStatusUI
from mmpe.ui.text_ui import TextUI, TextOutputUI, TextStatusUI


def compare(a, b):
    methods = lambda obj : set([m for m in dir(obj) if not m.startswith('_') and isinstance(getattr(obj, m), (FunctionType, MethodType))])

    for m in methods(a):
        a_args_spec = inspect.getargspec(getattr(a, m))

        b_args_spec = inspect.getargspec(getattr(b, m))
        for spec in ['args', 'varargs', 'keywords', 'defaults']:
            a_spec = getattr(a_args_spec, spec)
            b_spec = getattr(b_args_spec, spec)
            if a_spec != b_spec:
                raise Exception(m, a_spec, b_spec)
    if methods(a) - methods(b):
        raise Exception (a, b, methods(a) - methods(b))
    if methods(b) - methods(a):
        raise Exception (b, a, methods(b) - methods(a))

class Test(unittest.TestCase):


    def test_daemon_text(self):
        compare(TextUI, DaemonUI)

    def test_text_qt_output(self):

        compare(TextOutputUI(), QtOutputUI())

    def test_text_qt_status(self):
        app = QApplication([])
        compare(TextStatusUI(), QtStatusUI(None))


#    def test_text_qt(self):
#        app = QApplication([])
#        qt = QtUI(parent=None)
#        text = TextUI
#        self.assertFalse(compare(text, qt))
#        self.assertFalse(compare(qt, text))
#        #self.assertFalse(set(dir(text)) - set(dir(qt)))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
