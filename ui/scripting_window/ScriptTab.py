import os

from qtpy.QtCore import Qt, QEvent
from qtpy.QtWidgets import QMessageBox, QGridLayout, QWidget
from qtpy.QtGui import QFont, QFontMetrics, QColor, QKeyEvent

from Qsci import QsciScintilla, QsciLexerPython, QsciAPIs


#from model.Simulation import *
class ScriptTab(QWidget,):
    autocomplete_lst = []

    def __init__(self, parent, name, script="", filemodified=0):
        QWidget.__init__(self)
        self.parent = parent
        self.tabWidget = self.parent.ui.tabWidget
        self.gridlayout = QGridLayout(self)
        self._dirty = False

        self.initialize_editor()
        self.gridlayout.addWidget(self.editor)

        self.setAcceptDrops(True)

        self.filename = name
        self.filemodified = filemodified
        if self.is_file():
            self.title = os.path.basename(name)
            # if self.equals_saved():
            #    self.filemodified = os.path.getmtime(self.filename)
        else:
            self.filename = ""
            self.title = name

        # Show this file in the self.editor
        self.editor.setText(script)
        self.clean_txt = self.saved()

        self.update_dirty()

        self.editor.keyPressEvent = self.key_press_event

    @property
    def scriptRunner(self):
        return self.parent.controller.scriptRunner

    def wheelEvent(self, event):
        if event.modifiers() == Qt.ControlModifier:
            if event.delta() > 0:
                self.editor.zoomIn()
            else:
                self.editor.zoomOut()
        return QWidget.wheelEvent(self, event)


    def initialize_editor(self):



        self.editor = QsciScintilla()

#        self.editor.cursorPositionChanged.connect(self.e)
#        self.editor.copyAvailable.connect(self.e)
#        self.editor.indicatorClicked.connect(self.e)
#        self.editor.indicatorReleased.connect(self.e)
#        self.editor.linesChanged.connect(self.e)
#        self.editor.marginClicked.connect(self.e)
#        self.editor.modificationAttempted.connect(self.e)
#        self.editor.modificationChanged.connect(self.e)
#        self.editor.selectionChanged.connect(self.e)
#        self.editor.textChanged.connect(self.e)
#        self.editor.userListActivated.connect(self.e)

        if self.editor.__class__.__name__ == "LineTextWidget":
            return  # When using PySide without QSciScintilla

        # define the font to use
        font = QFont()
        font.setFamily("Consolas")
        font.setFixedPitch(True)
        font.setPointSize(10)
        # the font metrics here will help
        # building the margin width later
        fm = QFontMetrics(font)

        # set the default font of the self.editor
        # and take the same font for line numbers
        self.editor.setFont(font)
        self.editor.setMarginsFont(font)

        # Line numbers
        # conventionnaly, margin 0 is for line numbers
        self.editor.setMarginWidth(0, fm.width("00000") + 5)
        self.editor.setMarginLineNumbers(0, True)

        self.editor.setTabWidth(4)

        # Folding visual : we will use boxes
        self.editor.setFolding(QsciScintilla.BoxedTreeFoldStyle)

        self.editor.setAutoIndent(True)

        # Braces matching
        self.editor.setBraceMatching(QsciScintilla.SloppyBraceMatch)

        # Editing line color
        self.editor.setCaretLineVisible(True)
        self.editor.setCaretLineBackgroundColor(QColor("#CDA869"))

        # Margins colors
        # line numbers margin
        self.editor.setMarginsBackgroundColor(QColor("#333333"))
        self.editor.setMarginsForegroundColor(QColor("#CCCCCC"))

        # folding margin colors (foreground,background)
        self.editor.setFoldMarginColors(QColor("#99CC66"), QColor("#333300"))

        # Choose a lexer
        self.lexer = QsciLexerPython()
        self.lexer.setDefaultFont(font)

        # Set the length of the string before the editor tries to autocomplete
        # In practise this would be higher than 1
        # But its set lower here to make the autocompletion more obvious
        self.editor.setAutoCompletionThreshold(1)
        # Tell the editor we are using a QsciAPI for the autocompletion
        self.editor.setAutoCompletionSource(QsciScintilla.AcsAPIs)

        self.editor.setLexer(self.lexer)
        self.editor.setCallTipsStyle(QsciScintilla.CallTipsContext)

        # self.editor.setCallTipsVisible(0)
        # Create an API for us to populate with our autocomplete terms
        self.api = QsciAPIs(self.lexer)

        # Compile the api for use in the lexer
        self.api.prepare()




#    def tefocusInEvent(self, event):
#        self.parent.focusInEvent(event)
#        return QTextEdit.focusInEvent(self.textEditScript, event)

    def is_file(self):
        return os.path.isfile(self.filename)

    def is_modified(self):
        if self.is_file():
            if self.equals_saved():
                self.filemodified = os.path.getmtime(self.filename)
            return str(os.path.getmtime(self.filename)) != str(self.filemodified)
        else:
            return False

    def saved(self):
        if self.is_file():
            f = open(self.filename)
            saved = f.read()
            f.close()
            return saved.strip()
        else:
            return ""

    def equals_saved(self):
        curr_lines = self.get_script().strip().splitlines()
        saved_lines = self.saved().strip().splitlines()
        if len(curr_lines) != len(saved_lines):
            return False
        for cl, sl in zip(curr_lines, saved_lines):
            if cl.strip() != sl.strip():
                return False
        return True


    @property
    def dirty(self):
        if not self._dirty:
            self.dirty = self.clean_txt != self.get_script()
        return self._dirty

    @dirty.setter
    def dirty(self, dirty):
        if dirty is False:
            self.clean_txt = self.get_script()
        if self._dirty != dirty:
            self._dirty = dirty
            self.filename_changed()

    def update_dirty(self):
        return self.dirty

    def index(self):
        return self.tabWidget.indexOf(self)

    def filename_changed(self):
        index = self.parent.ui.tabWidget.indexOf(self)
        if self.dirty:
            self.tabWidget.setTabText(index, "%s*" % self.title)
        else:
            self.tabWidget.setTabText(index, self.title)

    def reload(self):
        self.set_script(self.parent._load_script(self.filename))
        self.filemodified = os.path.getmtime(self.filename)

    def close(self):
        while self.dirty is True:  # While avoids data loss, in case save operation is aborted
            if self.filename == "":
                text = "Save unsaved changes?"
            else:
                text = "Save %s?" % self.filename

            ans = QMessageBox.question(self, 'Save', text, QMessageBox.Yes, QMessageBox.Cancel, QMessageBox.No)

            if ans == QMessageBox.Cancel:
                return
            elif ans == QMessageBox.Yes:
                self.parent.actionSave()
            elif ans == QMessageBox.No:
                break
        self.tabWidget.removeTab(self.index())

    def _save(self,):
        f = open(self.filename, 'w')
        f.write(self.get_script())
        f.close()
        self.title = os.path.basename(self.filename)
        self.dirty = False



    def key_press_event(self, event):

        self.update_dirty()
        if self.editor.__class__.__name__ == "LineTextWidget":
            return self.editor.edit.keyReleaseEvent(event)  # When using PySide without QSciScintilla

        QsciScintilla.keyPressEvent(self.editor, event)

        linenr, pos_in_line = self.editor.getCursorPosition()
        line = str(self.editor.text(linenr)[:pos_in_line])

        if event.key() == Qt.Key_F1:
            try:
                self.parent.show_documentation(getattr(self.scriptRunner, str(self.editor.selectedText())))
            except AttributeError:
                pass

        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            for tip in self.autocomplete_lst:
                try:
                    if line.endswith(tip[:tip.index('(') ]):
                        self.editor.insert(tip[tip.index('('):])
                        parent, residual = self.scriptRunner.split_line(line)
                        self.parent.show_documentation(self.scriptRunner.get_function_dict(parent, residual)[residual])
                        return
                except ValueError:
                    pass

        if event.key() < 100 or event.key() in [Qt.Key_Backspace, Qt.Key_Shift]:
            linenr, pos_in_line = self.editor.getCursorPosition()
            line = str(self.editor.text(linenr)[:pos_in_line])

            lst = self.scriptRunner.get_autocomplete_list(line)

            if lst is not None:
                self.api.clear()
                list(map(self.api.add, lst))
                self.api.prepare()
                if len(lst) > 0:
                    self.autocomplete_lst = lst

            self.editor.autoCompleteFromAll()
            shift_event = QKeyEvent(QEvent.KeyPress, Qt.Key_Shift, Qt.NoModifier)
            QsciScintilla.keyPressEvent(self.editor, shift_event)  # show autocomplete list




    def set_script(self, script):
        self.editor.setText(script)

    def get_script(self):
        return str(self.editor.text()).replace("\r", "").replace(">>> ", "").replace("\t", "    ")

    def dropHandler(self, dataItemList, ctrl, shift, event):
        pass
