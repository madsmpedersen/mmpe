'''
Created on 24/04/2013

@author: Mads M. Pedersen (mmpe@dtu.dk)
'''

from PyQt4 import QtCore
import time


last_time = {}
last_duration = {}


def wait_for_last(f):
    def wrap(*args, **kwargs):
        t = time.time()
        if f in last_time and t - last_time[f] < last_duration[f] * 1.1:
            return
        ret = f(*args, **kwargs)
        last_time[f] = t
        last_duration[f] = time.time() - t
        return ret
    return wrap






class WaitThread(QtCore.QThread):
    done = QtCore.pyqtSignal(object)

    def __init__(self, duration):
        QtCore.QThread.__init__(self)
        self.duration = duration

    def run(self):
        time.sleep(self.duration)
        self.done.emit(self)


class HoldIt(object):
    _waiting = False

    def __init__(self, f):
        self.f = f
        self.update_duration = 0
        self.last_call = 0
        self.waitThread_pool = []

    def hold_it(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        now = time.time()
        wait_sec = max(0, self.last_call + self.update_duration - now)
        if not self._waiting:
            self._waiting = True
            waitThread = WaitThread(wait_sec)
            self.waitThread_pool.append(waitThread)
            waitThread.done.connect(self.do_it)
            waitThread.start()

    def do_it(self, waitThread):
        self._waiting = False
        for t in self.waitThread_pool:
            if t.isFinished():
                self.waitThread_pool.remove(t)
        self.last_call = time.time()
        self.f(*self.args, **self.kwargs)
        duration = time.time() - self.last_call
        if duration > 0:
            self.update_duration = duration


holdit_objs = {}


def postpone_until_last_call_finishes(f):
    def wrapper(*args, **kwargs):
        if f not in holdit_objs:
            holdit_objs[f] = HoldIt(f)
        holdit_objs[f].hold_it(*args, **kwargs)
    return wrapper
