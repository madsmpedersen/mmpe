'''
Classes for loading a QWidget designed in QT Designer as MainWindow, Dialog or Widget
Examples of how to use can be found in UseQtGuiLoader.py

@Created on 13/3/2013
@modified
@version:1.9 (18/2-2014)
@change: 1.8 Compile code changed again
             Autogeneration of missing action handlers
         1.8 os.environ.get('path', "") instead of os.environ['path'] to avoid error if path variable not exists (e.g. on linux)
         1.7 Supports both PyQt4 and PySide
         1.6 python + python/scripts path appended to os.environ['path']
             'WINPYDIR' appended to os.environ
             basename set relative to cwd
         1.5 changed sys.exit(app.exec_()) to app.exec_() to avoid SystemExit exception when running from IPython
             Gridlayout with ui_widget added to QtWidgetLoader
             application argument removed
         1.4 Actions can be connected to methods of same name if they exists by calling 'connect_actions'
             _ui_widget set to last child of action_receiver with name 'QWidget' instead of last child
         1.3 QtWidgetLoader.new() returns MyWidget instead of QWidget
         1.2 QtMainWindowLoader now works on Widget and MainWindow
             Actions are connected to methods of same name if they exists
         1.1 copy attributes from mmpe.QtGuiLoader to qtGuiLoader.widget
@author: Mads M Pedersen (mmpe@dtu.dk)
'''


from PyQt4 import QtGui, QtCore
import os
import sys
import imp
import inspect
from mmpe.functions import exe_std_err
from mmpe.QtGuiLoader import CleanMainWindowUI


def pyqt_compile_func(ui_file, py_file):
    pyuic_path = os.path.join(os.path.dirname(sys.executable), 'Lib/site-packages/PyQt4/uic/pyuic.py')
    os.system('"%s" %s %s > %s' % (sys.executable, pyuic_path, ui_file, py_file))


class QtGuiLoader(object):

    def compile_ui(self, ui_module, recompile=False):
        basename = os.path.relpath(os.path.splitext(ui_module.__file__)[0], os.getcwd())
        ui_file = basename + ".ui"
        py_file = basename + ".py"

        if os.path.exists(ui_file):
            if not os.path.exists(py_file) or \
                os.path.getmtime(ui_file) > os.path.getmtime(py_file) or \
                os.path.getsize(py_file) == 0 or \
                recompile:
                print ("compile %s > %s" % (ui_file, py_file))
                exe_dir = os.path.dirname(sys.executable)

                #ui_compile_func(ui_file, py_file)
                #os.system("%s %s > %s" % (ui_compiler, ui_file, py_file))
#                pyuic_path = os.path.join(os.path.dirname(sys.executable), 'Lib/site-packages/PyQt4/uic/pyuic.py')
#                os.system("%s %s %s > %s" % (sys.executable, pyuic_path, ui_file, py_file))
                pyqt_compile_func(ui_file, py_file)
        imp.reload(ui_module)

    def connect_actions(self, action_receiver=None):
        if not hasattr(self, 'run') and hasattr(self.parent(), 'run'):
            self.run = self.parent().run
        for name, action in [(n, a) for n, a in vars(self.ui).items() if isinstance(a, QtGui.QAction)]:
            if action_receiver is None:
                action_receiver = self
            if hasattr(action_receiver, "_" + name) and hasattr(self, "run") and hasattr(self, 'gui'):
                func = getattr(action_receiver, "_" + name)
                def action_wrapper(f):
                    def wrapper(*args, **kwargs):
                        return self.gui.run(f, *args, **kwargs)
                    return wrapper

                setattr(action_receiver, name, action_wrapper(func))

            if hasattr(action_receiver, name):
                QtCore.QObject.connect(action, QtCore.SIGNAL("triggered()"), getattr(action_receiver, name))
            elif not hasattr(action_receiver, "_" + name):
                try:
                    source_file = inspect.getsourcefile(self.__class__)
                    class_source = inspect.getsource(self.__class__)
                    func_source = """
    def _%s(self):
        #Auto implemented action handler
        raise NotImplementedError
""" % name

                    with open(source_file, 'r+') as fid:
                        source = fid.read().replace(class_source, class_source + func_source)
                        fid.seek(0)
                        fid.write(source)
                    print ("Missing method '_%s' appended to class %s" % (name, self.__class__.__name__))
                except:
                    raise Warning("Action %s not connected. Method with name '%s' not found and autogeneration failed" % (action.text(), name))

    def setupUI(self, widget):
        self.ui.setupUi(widget)
        root_widgets = [w for w in widget.children() if w.__class__.__name__ == "QWidget"]
        if len(root_widgets) == 0 or widget.layout() is not None:
            self.ui_widget = self
        else:
            self.ui_widget = root_widgets[-1]
            g = QtGui.QGridLayout()
            if isinstance(self, QtWidgetLoader):
                g.setMargin(0)
                g.setSpacing(0)
            widget.setLayout(g)

            g.addWidget(self.ui_widget)


class QtGuiApplication(object):

    def __init__(self, ui_module):
        self.ui_module = ui_module
        self.app_filename = os.path.basename(sys.argv[0])
        self.app_name = os.path.splitext(self.app_filename)[0]
        if QtGui.QApplication.startingUp():
            self.app = QtGui.QApplication(sys.argv)
        if not hasattr(self.ui_module, '__name__'):
            self.ui_module.__name__ = self.ui_module.__class__.__name__
        if hasattr(self, 'compile_ui'):
            self.compile_ui(ui_module)

    def save_settings(self):
        settings = QtCore.QSettings("QtGuiApplication", "%s_%s" % (self.app_name, self.__class__.__name__))
        settings.setValue(self.ui_module.__name__ + "/geometry", self.saveGeometry())

    def load_settings(self):
        settings = QtCore.QSettings("QtGuiApplication", "%s_%s" % (self.app_name, self.__class__.__name__))
        geometry = settings.value(self.ui_module.__name__ + "/geometry")
        try:
            geometry = geometry.toByteArray()
        except:
            pass  # Fails in PySide
        if geometry:
            self.restoreGeometry(geometry)

    def save_setting(self, key, value):
        settings = QtCore.QSettings("QtGuiApplication", "%s_%s" % (self.app_name, self.__class__.__name__))
        settings.setValue(self.ui_module.__name__ + "/" + key, value)

    def load_setting(self, key, default_value=None):
        settings = QtCore.QSettings("QtGuiApplication", "%s_%s" % (self.app_name, self.__class__.__name__))
        setting = settings.value(self.ui_module.__name__ + "/" + key, default_value)
        try:
            setting = setting.toString()
        except:
            pass  #fails in pyside
        return str(setting)

    def clear_settings(self):
        settings = QtCore.QSettings("QtGuiApplication", "%s_%s" % (self.app_name, self.__class__.__name__))
        settings.clear()


class QtMainWindowLoader(QtGuiLoader, QtGuiApplication, QtGui.QMainWindow):
    """Load QtGui as MainWindow

    Examples
    --------

    class MyMainWindow(QtMainWindowLoader):
        def __init__(self, parent=None):
            ui_module = MyWidgetUI
            try: self.ui = ui_module.Ui_Form()  #enable autocomplete
            except: pass
            QtMainWindowLoader.__init__(self, ui_module)
            self.ui.lineEdit.setText("MyMainWindow")
            self.setWindowTitle("MyMainWindow")

        def actionPrintText(self):
            print ("Mainwindow text: %s" % self.ui.lineEdit.text())
    """

    def __init__(self, ui_module=CleanMainWindowUI, connect_actions=True):

        self.gui = self
        QtGuiApplication.__init__(self, ui_module)
        QtGui.QMainWindow.__init__(self)

        if "Ui_Form" in dir(ui_module):
            self.ui = ui_module.Ui_Form()
            centralWidget = QtGui.QWidget(self)
            self.setCentralWidget(centralWidget)
            try:
                self.setupUI(centralWidget)
            except TypeError:
                self.compile_ui(ui_module, True)
                self.ui = ui_module.Ui_Form()
                self.setupUI(centralWidget)
#
        elif "Ui_MainWindow" in dir(ui_module):
            self.ui = ui_module.Ui_MainWindow()

            try:
                self.ui.setupUi(self)
            except TypeError:
                self.compile_ui(ui_module, True)
                self.ui = ui_module.Ui_MainWindow()
                self.ui.setupUi(self)

        if connect_actions:
            self.connect_actions()


    def start(self):
        self.load_settings()

        self.show()
        if hasattr(self, "app"):
            QtCore.QTimer().singleShot(100, self.post_initialize)
            self.app.aboutToQuit.connect(self.cleanUp)
            self.app.exec_()

    def post_initialize(self):
        pass

    def cleanUp(self):
        def clean(item):
            """Clean up the memory by closing and deleting the item if possible."""
            if isinstance(item, list):
                while (len(item)):
                    clean(item.pop())
            elif isinstance(item, dict):
                while (len(item)):
                    clean(item.popitem())
            else:
                try:
                    item.close()
                except (RuntimeError, AttributeError):  # deleted or no close method
                    pass
                try:
                    item.deleteLater()
                except (RuntimeError, AttributeError):  # deleted or no deleteLater method
                    pass

        for i in list(self.__dict__.keys()):
            if i in self.__dict__:
                item = self.__dict__[i]
                clean(item)


    def terminate(self):
        QtGui.QApplication.quit()

    def closeEvent(self, *args, **kwargs):
        self.save_settings()
        # Enable paste of clipboard after termination
        clipboard = QtGui.QApplication.clipboard()
        event = QtCore.QEvent(QtCore.QEvent.Clipboard)
        QtGui.QApplication.sendEvent(clipboard, event)
        return QtGui.QMainWindow.closeEvent(self, *args, **kwargs)


class QtDialogLoader(QtGuiLoader, QtGuiApplication, QtGui.QDialog):

    def __init__(self, ui_module, parent, modal=True, connect_actions=True):
        self.gui = parent
        QtGuiApplication.__init__(self, ui_module)
        QtGui.QDialog.__init__(self, parent)
        self.modal = modal
        self.setModal(modal)
        try:
            self.ui = ui_module.Ui_Form()
            self.setupUI(self)
        except:
            self.compile_ui(ui_module, True)
            self.ui = ui_module.Ui_Form()
            self.setupUI(self)

        if connect_actions:
            self.connect_actions()

    def start(self):
        self.load_settings()
        self.show()
        self.raise_()
        if hasattr(self, "app"):
            return self.app.exec_()
        elif self.modal:
            return self.exec_()

    def hideEvent(self, *args, **kwargs):
        self.save_settings()
        if isinstance(self, QtGui.QDialog):
            return QtGui.QDialog.hideEvent(self, *args, **kwargs)



class QtWidgetLoader(QtGuiLoader, QtGui.QWidget):

    def __init__(self, ui_module, action_receiver=None, parent=None, connect_actions=True):
        if "ui_module" not in vars(self):
            QtGui.QWidget.__init__(self, parent)
            self.gui = parent
            self.ui_module = ui_module
            self.compile_ui(ui_module)
            self.ui = ui_module.Ui_Form()
            try:
                self.setupUI(self)
            except:
                self.compile_ui(ui_module, True)
                self.ui = ui_module.Ui_Form()
                self.setupUI(self)


            if connect_actions:
                self.connect_actions(action_receiver)

    def _actionApply(self):
        #Auto implemented action handler
        raise NotImplementedError
