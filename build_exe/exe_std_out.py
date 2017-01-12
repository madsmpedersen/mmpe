import os
import sys

class ExeStdOut(object):
    def __init__(self, *args):
        self.filename = 'std_out.out'
        sys.stdout = self
        if args:
            self.write(" ".join([str(arg) for arg in args]))

    def write(self, s):
        try:
            with open(os.path.realpath(self.filename), 'a') as fid:
                fid.write(s + "\n---------\n")

            sys.__stdout__.write("exestdout: %s\n" % s)
            sys.__stdout__.flush()
        except:
            pass

    def clear(self):
        try:
            with open(os.path.realpath(self.filename), 'w'):
                pass
        except:
            pass

    def flush(self):
        pass
