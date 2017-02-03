from mmpe.build_exe import exe_std_out
from mmpe.functions.exe_std_out import ExeStdOut
from mmpe.QtGuiLoader.QtGuiLoader import QtMainWindowLoader
from mmpe.ui.qt_ui import QtUI, QtInputUI

from multiprocessing import Process
import os
import re
import sys
from mmpe.ui.scripting_window.script_function import ScriptFunction
import inspect


import time
import traceback
import PyQt4
#
from PyQt4.QtCore import Qt, QUrl
from PyQt4.QtGui import QMessageBox, QDialog, QFileDialog, QIcon, QApplication
from mmpe.QtGuiLoader import QtDialogLoader
from mmpe.datastructures.Singleton import singleton
from mmpe.ui.scripting_window import SimpleScriptingWindowUI as ScriptingWindowUI
from mmpe.ui.scripting_window.ScriptRunner import ScriptRunner
from mmpe.ui.scripting_window.ScriptTab import ScriptTab
from mmpe.ui.text_ui import TextUI
from mmpe.functions.deep_coding import to_str
from mmpe.io.make_dirs import make_dirs
from mmpe.functions.timing import print_cum_time


def beep(frq=2500, dur=50):
    if sys.platform == 'win32':
        import winsound
        winsound.Beep(frq, dur)




 
class ScriptingWindow(QtInputUI):

    autosave_splitter = """
#===============================================================================
# Autosave
#===============================================================================
"""

    autosave_filename = os.path.expanduser('~/.tmp/autosave.py')
    autosave_warning_shown = False
    handle_focus = False
    anchor = None

    def __init__(self, controller, gui, model, appfuncs_path="appfuncs"):
        QtInputUI.__init__(self, gui)
        self.font_size = 10
        self.controller = controller
        self.model = model
        self.gui = gui
        self.appfuncs_path = appfuncs_path
        make_dirs(self.autosave_filename)
        self.load_autosave()
        self.ui.splitter.setSizes([400, 200])
        self.ui.splitter_2.setSizes([800, 400])

        # self.setAcceptDrops(True)
        self.setFocusPolicy(Qt.StrongFocus)
        self.ui.tabWidget.setFocusPolicy(Qt.StrongFocus)
        self.ui.tabWidget.focusInEvent = self.focusInEvent
        self.ui.tabWidget.tabCloseRequested.connect(self.close_tab)
        self.ui.tabWidget.currentChanged.connect(self.tab_changed)
        self.setWindowIcon(QIcon('graphics/Pdap.ico'))




    def tab_changed(self, index):
        pass



    def loadstarted(self):
        print ("load start", self.ui.webView.url())

    @property
    def scriptRunner(self):
        return self.controller.scriptRunner


    def focusInEvent(self, event):
        if self.handle_focus:
            self.handle_focus = False
            tab = self.ui.tabWidget.currentWidget()
            if tab is not None and tab.is_modified():
                msg = 'The file \'%s\' has been changed on the file system. Do you want to replace the editor contents with these changes?' % tab.filename
                msg += "\n\n" + "\n".join(["Diff in line %d:\nIn script: %s\nIn file:   %s\n" % (lnr, l1, l2) for lnr, (l1, l2) in enumerate(zip(tab.get_script().split("\n"), tab.saved().split("\n"))) if l1.strip() != l2.strip()][:5])
                if QMessageBox.information(self, 'File changed', msg, QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
                    tab.reload()
                else:
                    tab.filemodified = os.path.getmtime(tab.filename)
            self.handle_focus = True

    def autosave(self):
        s = []
        for i in range(self.ui.tabWidget.count()):
            tab = self.ui.tabWidget.widget(i)
            s.append("%s#%s\n#%s\n%s" % (self.autosave_splitter, tab.filename, tab.filemodified, tab.get_script()))
        try:
            with open(self.autosave_filename, 'w') as fid:
                fid.write("".join(s))
        except IOError:
            if self.autosave_warning_shown is False:
                self.autosave_warning_shown = True
                self.gui.show_warning("Temporary scripts could not be saved automatically\n\nPermission denied to: '%s'" % os.path.realpath(self.autosave_filename))

    def load_autosave(self):

        autosave = self._load_script(self.autosave_filename)
        scripts = autosave.split(self.autosave_splitter)
        for s in scripts[1:]:
            filename = s.splitlines()[0][1:]
            filemodified = float(s.splitlines()[1][1:])
            script = "\n".join(s.splitlines()[2:])
            tab = self._actionNew(filename, script, filemodified)
            #tab.dirty = not tab.equals_saved()
        if self.ui.tabWidget.count() == 0:
            self._actionNew()

    def close(self):
        self.autosave()

    def new_tab(self, filename="New", script=""):
        self._actionNew(filename, script)

    def _actionNew(self, filename="New", script="", filemodified=0):
        tab = ScriptTab(self, filename, script, filemodified)
        self.ui.tabWidget.addTab(tab, tab.title)
        tab.filename_changed()
        self.ui.tabWidget.setCurrentIndex(self.ui.tabWidget.count() - 1)
        return tab

    def _actionRunScript(self):
        self.autosave()
        script = self.ui.tabWidget.currentWidget().get_script()
        self.run_script(script)

    def run_script(self, script):
        self.gui.start_wait()
        self.set_output("")
        self.ui.labelLineNumber.setText("")
        QApplication.processEvents()
        sys.stdout = self
        starttime = -time.time()

        try:

            self.output = []
            self.scriptRunner.run(script)
            self.set_output("".join(self.output))
        except (Warning, Exception) as inst:
            traceback.print_exc(file=sys.stdout)
            self.set_output("".join(self.output))
            sys.stdout = sys.__stdout__
            try:
                linenr = self.output[[self.output.index(l) for l in self.output if "File \"<string>\", line " in l][-1]]
                linenr = linenr[23:]
                if "," in linenr:
                    linenr = int(linenr[:linenr.index(",")])
                else:
                    linenr = int(linenr)

                self.selectLine(linenr - 1)
            except IndexError:
                pass
            print ('-' * 60)
            beep(500, 50)
        finally:

            sys.stdout = sys.__stdout__
        self.ui.labelLineNumber.setText("Script executed in %d seconds" % (time.time() + starttime))
        self.gui.end_wait()

    def write(self, s):
        try:
            sys.__stdout__.write(s)
        except (IOError, AttributeError):
            #flush not working in no console cx_freeze application
            # __stdout__ is None and has no write method in cx_freeze application
            pass
        self.output.append(s)



    def flush(self):
        pass  # solves problem on linux

    def selectLine(self, linenr):
        self.ui.tabWidget.currentWidget().editor.setSelection(linenr, 0, linenr, -1)
        self.ui.tabWidget.currentWidget().editor.ensureLineVisible(linenr)


    def _exec(self, script):
        exec(script)

#    def updateElapsed(self):
#        self.elapsed += 1
#        print (self.elapsed)
#        self.ui.labelLineNumber.setText("Elapsed: %d" % self.elapsed)

    def close_tab(self, index):
        self.ui.tabWidget.setCurrentIndex(index)
        self.ui.tabWidget.widget(index).close()
        if self.ui.tabWidget.count() == 0:
            self._actionNew()

    def _actionOpen(self, filename=""):
        if filename == "":
            filename = self.get_open_filename("Open script", "*.py")
            if filename == '':
                return
        if os.path.isfile(filename):
            self._actionNew(filename, self._load_script(filename), os.path.getmtime(filename))

    def _actionSave(self):
        tab = self.ui.tabWidget.currentWidget()
        if os.path.isfile(tab.filename):
            tab._save()
        else:
            self._actionSaveAs()

    def _actionSaveAs(self):
        filename = self.get_save_filename("Save script", "*.py")
        if filename != "":
            self.ui.tabWidget.currentWidget().filename = filename
            try:
                f = open(filename, 'w')
                f.close()
            except:
                pass
            self._actionSave()

    def _actionImportPlugin(self, plugin_filename=None):
        self.close()
        if plugin_filename is None:
            plugin_filename = self.get_open_filename("Open plugin file", "*.py")
        if os.path.isfile(plugin_filename):
            f = open(plugin_filename)
            plugin = f.read()
            f.close()

            def is_plugin(plugin):
                return re.compile('class [\w ]*\([\w, ]*Plugin[\w, ]*\):[^\b]*def run\(self\):\n        ').search(plugin)

            r = is_plugin(plugin)
            if r is None:

                QMessageBox.warning(self, "Import error", "Script in \n\n%s\n\ncould not be identified as a plugin" % plugin_filename, QMessageBox.Ok)
            else:
                script = plugin[r.end():].replace("\n        ", "\n")
                self.set_script(script)


    def load_script(self):
        self._load_script(self.filename)

    def _load_script(self, filename):
        try:
            f = open(filename)
            script = f.read()
            f.close()
            return script
        except:
            return ""

    def set_output(self, output):
        self.ui.textEditOutput.setText(output)

    def set_position(self, line):
        self.ui.labelLineNumber.setText("Line: %d" % line)

    def get_obj(self, name):
        try:
            return eval(name)
        except:
            return None



class Seq_Script(Process):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}):
        Process.__init__(self, group=group, target=target, name=name, args=args, kwargs=kwargs)

@singleton
class ScriptingDialogWindow(ScriptingWindow, QtDialogLoader):
    def __init__(self, controller, gui, model):
        module = ScriptingWindowUI
        try: self.ui = module.Ui_Form()
        except: pass
        QtDialogLoader.__init__(self, module, gui, modal=False)
        self.setParent(None)
        ScriptingWindow.__init__(self, controller, gui, model)
        self.setModal(False)

    def closeEvent(self, *args, **kwargs):
        self.close()
        return QtDialogLoader.closeEvent(self, *args, **kwargs)

    def _actionExportPlugin(self):
        #Auto implemented action handler
        raise NotImplementedError


class ScriptingMainWindow(QtMainWindowLoader, ScriptingWindow, QtUI):

    def __init__(self, controller, model):
        module = ScriptingWindowUI
        try: self.ui = module.Ui_Form()
        except: pass

        QtMainWindowLoader.__init__(self, module, self)
        ScriptingWindow.__init__(self, controller, self, model)
        QtUI.__init__(self, self)

    def closeEvent(self, *args, **kwargs):
        self.close()
        return QtMainWindowLoader.closeEvent(self, *args, **kwargs)

    def _actionExportPlugin(self):
        #Auto implemented action handler
        raise NotImplementedError


class ScriptingController(object):
    def __init__(self):
        self.gui = ScriptingMainWindow(self, None)
        self.scriptRunner = ScriptRunner(self, self.gui, None)

if __name__=="__main__":
    c = ScriptingController()
    c.gui.start()
    

