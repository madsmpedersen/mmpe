import os

from mmpe.functions.exe_std_out import ExeStdOut
import sys


try:
    import win32ui
    win32ui_exists = True
except:
    win32ui_exists = False

class ExeStdErr(ExeStdOut):
    user_informed = False

    def __init__(self):
        self.filename = 'std_err.out'
        sys.stderr = self


    def __del__(self):
        sys.stderr = sys.__stderr__



    def write(self, s):
        try:
            with open(os.path.realpath(self.filename), 'a') as fid:
                fid.write(s + "\n---------\n")
            print  ("Error", s,)
            if win32ui_exists and not self.user_informed:
                if os.path.isfile(os.path.realpath('std_err.out')):
                    win32ui.MessageBox("An error has occured. The error message has been written to:\n%s" % os.path.realpath('std_err.out'), "Error occured")
                else:
                    win32ui.MessageBox("An error has occured. Could not create error log", "Error occured")
                self.user_informed = True
        except:
            pass
