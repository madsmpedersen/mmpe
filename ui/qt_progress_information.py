


import collections
import inspect
import sys
from threading import Thread
import threading
import time

from qtpy.QtCore import Qt
from qtpy import QtCore
from qtpy.QtWidgets import QMainWindow
from qtpy.QtWidgets import QProgressDialog, QApplication


# try:
#     from pyqt.QtCore import QString
# except:
#     QString = str
class CancelWarning(Warning):
    pass
class TaskThread(Thread):
    result = None
    def __init__(self, task, *args, **kwargs):
        Thread.__init__(self)
        self.task = lambda: task(*args, **kwargs)

    def run(self):
        try:
            self.result = self.task()
        except Exception as e:
            self.result = e


class CancelableTaskThread(TaskThread):
    def __init__(self, task, *args, **kwargs):
        self.cancel_event = threading.Event()
        if "cancel_event" not in inspect.getargspec(task)[0]:
            raise TypeError("Cancelable tasks must take a 'cancel_event'-argument")
        kwargs['cancel_event'] = self.cancel_event
        TaskThread.__init__(self, task, *args, **kwargs)


class QtProgressInformation(object):
    def __init__(self, parent):
        self._parent = parent
        self._progressDialog = QProgressDialog(self._parent)
        self._progressDialog.setMinimumWidth(300)
        self._progressDialog.setWindowModality(Qt.ApplicationModal)
        self._progressDialog.setMinimumDuration(0)
        self._progressDialog.hide()
#        self.progress_iterator = lambda seq, text = "Working... Please wait", allow_cancel = True, self = self : self.QtProgressIterator(self, seq, text, allow_cancel)

    def progress_iterator(self, sequence, text="Working... Please wait", allow_cancel=True, always_refresh=True):
        return self.QtProgressIterator(self, sequence, text, allow_cancel)


    def __show(self, text, allow_cancel, max_value=0):
        if not hasattr(self, '_progressDialog'):
            raise Exception ("%s inheriting QtProgressInformation must call QtProgressInformation.__init__" % self.__class__.__name__)
        self._progressDialog.reset()  #reset cancel flag
        self._progressDialog.setWindowTitle(text)
        self._progressDialog.setMaximum(max_value)

        cancel_text = (None, "Cancel")[allow_cancel]
        self._progressDialog.setCancelButtonText(cancel_text)
        self._progressDialog
        self._progressDialog.show()
        QApplication.processEvents()

    def __hide(self):
        self._progressDialog.hide()
        self._progressDialog.close()
        QApplication.processEvents()

    def start_blocking_task(self, text):
        self.__show(text, False)

    def end_blocking_task(self):
        self.__hide()

    class QtProgressIterator(collections.Iterator):
        def __init__(self, QtProgressInformation, seq, text, allow_cancel=True):
            self.QtProgressInformation = QtProgressInformation
            self.generator = iter(list(seq))

            self.allow_cancel = allow_cancel
            self.n = 0

            max_value = self.generator.__length_hint__()
            self.update_every = max(1, max_value // 100)
            self.QtProgressInformation._QtProgressInformation__show(text, allow_cancel, max_value)


        def __del__(self):
                self.QtProgressInformation._QtProgressInformation__hide()
                pass

        def __iter__(self):
                return self

        def next(self):
            # required by python 2
            return self.__next__()

        def __next__(self):

            if self.n % self.update_every == 0:
                if self.allow_cancel and self.QtProgressInformation._progressDialog.wasCanceled():
                    raise CancelWarning()
                self.QtProgressInformation._progressDialog.setValue(self.n)
            self.n += 1

            try:
                return self.generator.__next__()
            except AttributeError:
                return self.generator.next()  #in python 2, iterators __next__ is named next


    def _callback(self, current, maximum):
        if self._progressDialog.maximum() != maximum:
            self._progressDialog.setMaximum(maximum)

        self._progressDialog.setValue(current)
        if self._progressDialog.wasCanceled():
            raise CancelWarning()



    def exec_long_task_with_callback(self, text, allow_cancel, task, *args, **kwargs):

        self.__show(text, allow_cancel)
        try:
            res = task(*args, **kwargs)
        except Exception as e:
            raise e
        finally:
#        self.taskThread = TaskThread(task, *args, **kwargs)
#        self.taskThread.cancel_event = threading.Event()
#        self.taskThread.start()
#        while self.taskThread.is_alive():
#            time.sleep(0.1)
#            if allow_cancel and self._progressDialog.wasCanceled():
#                self.taskThread.cancel_event.set()
#                self.taskThread.join()
#                #raise CancelWarning
#            QApplication.processEvents()
#        self.taskThread.join()
            self.__hide()
        return res

#    def progress_iterator(self, sequence, text="Working... Please wait", allow_cancel=True):
#        it = iter(sequence)
#        if it.__length_hint__() > 0:
#            self.__show(text, allow_cancel, it.__length_hint__())
#            for n, v in enumerate(it):
#                if allow_cancel and self._progressDialog.wasCanceled():
#                    raise CancelWarning()
#                self._progressDialog.setValue(n)
#                yield(v)
#            self._progressDialog.hide()
#            QApplication.processEvents()

    def exec_long_task(self, text, allow_cancel, task, *args, **kwargs):


#        class TaskQThread(QThread):
#            result = None
#            def __init__(self, _parent, task, *args, **kwargs):
#                QThread.__init__(self)
#                self.task = lambda: task(*args, **kwargs)
#
#            def run(self):
#                self.result = self.task()
#        t = TaskQThread(self, task, *args, **kwargs)
#        t.start()
#        while t.isRunning():
#            time.sleep(0.1)
#            QApplication.processEvents()


        self.__show(text, allow_cancel)
        if allow_cancel:
            self.taskThread = CancelableTaskThread(task, *args, **kwargs)
        else:
            self.taskThread = TaskThread(task, *args, **kwargs)

        self.taskThread.start()
        while self.taskThread.is_alive():
            time.sleep(0.1)
            if allow_cancel and self._progressDialog.wasCanceled():
                self.taskThread.cancel_event.set()
                self.taskThread.join()
                raise CancelWarning
            QApplication.processEvents()
        self.taskThread.join()
        self.__hide()
        if isinstance(self.taskThread.result, Exception):
            raise self.taskThread.result
        return self.taskThread.result

    def exec_long_guitask(self, text, task, *args, **kwargs):
        self.__show(text, False)
        QApplication.processEvents()
        task(*args, **kwargs)
        self.__hide()



        return self.taskThread.result

def long_task(parent=None, text="Working", allow_cancel=False):
    def wrap(task):
        def taskWrapper(*args, **kwargs):
            return QtProgressInformation(parent).exec_long_task(text, allow_cancel, task, *args, **kwargs)
        return taskWrapper
    return wrap


#
if __name__ == "__main__":
    class MW(QMainWindow, QtProgressInformation):
        def __init__(self):
            QMainWindow.__init__(self)
            QtProgressInformation.__init__(self, self)


        def mouseDoubleClickEvent(self, *args, **kwargs):

            @long_task(self, "decorator(without cancel)", False)
            def task1a(sec):
                t = time.time()
                while time.time() - t < sec:
                    pass
                return "result of task1a"


            @long_task(self, "decorator(with cancel)", True)
            def task1b(sec, cancel_event):
                t = time.time()
                while time.time() - t < sec:
                    if cancel_event.isSet():
                        break
                return "result of task1b"

            def task2a(sec):
                t = time.time()
                while time.time() - t < sec:
                    pass
                return "result of task2a"

            def task2b(sec, cancel_event):
                t = time.time()
                while time.time() - t < sec:
                    if cancel_event.isSet():
                        break
                return "result of task2b"

            def task3a(callback, sec):
                t = time.time()
                while time.time() - t < sec:
                    callback(time.time() - t, t + sec)
                    time.sleep(.1)
                return "result of task2b"

            def task3b(callback, sec):
                try:
                    t = time.time()
                    while time.time() - t < sec:
                        callback(time.time() - t, t + sec)
                        #if cancel_event.isSet():
                        #    break
                        time.sleep(.1)
                    return "result of task2b"
                except CancelWarning:
                    return "Cancelled"
#
#            print (task1a(1))
#
#            try:
#                print (task1b(3))
#            except CancelWarning:
#                print ("task1b cancelled")
#
#
#            print (self.exec_long_task("exec_long_task(without cancel)", False, task2a, 1))
#
#            try:
#                print (self.exec_long_task("exec_long_task(with cancel", True, task2b, 5))
#            except CancelWarning:
#                print ("task2 cancelled")
#
#

            for x in self.progress_iterator(range(100), "progressbar(without cancel)", False):
                t = time.time()
                while time.time() - t < .01:
                    pass
                if x > 80:
                    raise Exception

            try:
                for _ in self.progress_iterator(range(100), "progressbar(with cancel)", True):
                    t = time.time()
                    while time.time() - t < .05:
                        pass
            except CancelWarning:
                print ("progressbar cancelled")
            return QMainWindow.mouseDoubleClickEvent(self, *args, **kwargs)

#            print (self.exec_long_task_with_callback("callback no cancel", allow_cancel=True, task=task3b, callback=self._callback, sec=5))



    app = QApplication(sys.argv)
    mw = MW()
    mw.show()
    sys.exit(app.exec_())

