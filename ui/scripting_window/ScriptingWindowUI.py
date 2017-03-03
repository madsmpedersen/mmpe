# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mmpe\ui\scripting_window\ScriptingWindowUI.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.setWindowModality(QtCore.Qt.NonModal)
        Form.resize(624, 526)
        Form.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.gridLayout_2 = QtGui.QGridLayout(Form)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.menuBar = QtGui.QMenuBar(Form)
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.menuFile = QtGui.QMenu(self.menuBar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuRun = QtGui.QMenu(self.menuBar)
        self.menuRun.setObjectName(_fromUtf8("menuRun"))
        self.gridLayout_2.addWidget(self.menuBar, 0, 0, 1, 1)
        self.splitter_2 = QtGui.QSplitter(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter_2.sizePolicy().hasHeightForWidth())
        self.splitter_2.setSizePolicy(sizePolicy)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName(_fromUtf8("splitter_2"))
        self.layoutWidget = QtGui.QWidget(self.splitter_2)
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.splitter = QtGui.QSplitter(self.layoutWidget)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.verticalLayoutWidget = QtGui.QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.tabWidget = QtGui.QTabWidget(self.verticalLayoutWidget)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.verticalLayout_2.addWidget(self.tabWidget)
        self.verticalLayoutWidget_2 = QtGui.QWidget(self.splitter)
        self.verticalLayoutWidget_2.setObjectName(_fromUtf8("verticalLayoutWidget_2"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.label_2 = QtGui.QLabel(self.verticalLayoutWidget_2)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_3.addWidget(self.label_2)
        self.textEditOutput = QtGui.QTextEdit(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Consolas"))
        font.setPointSize(9)
        self.textEditOutput.setFont(font)
        self.textEditOutput.setAcceptDrops(False)
        self.textEditOutput.setReadOnly(True)
        self.textEditOutput.setObjectName(_fromUtf8("textEditOutput"))
        self.verticalLayout_3.addWidget(self.textEditOutput)
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)
        self.webView = QtWebKit.QWebView(self.splitter_2)
        self.webView.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.webView.setObjectName(_fromUtf8("webView"))
        self.gridLayout_2.addWidget(self.splitter_2, 1, 0, 1, 1)
        self.labelLineNumber = QtGui.QLabel(Form)
        self.labelLineNumber.setText(_fromUtf8(""))
        self.labelLineNumber.setObjectName(_fromUtf8("labelLineNumber"))
        self.gridLayout_2.addWidget(self.labelLineNumber, 2, 0, 1, 1)
        self.actionSaveAs = QtGui.QAction(Form)
        self.actionSaveAs.setObjectName(_fromUtf8("actionSaveAs"))
        self.actionRunScript = QtGui.QAction(Form)
        self.actionRunScript.setObjectName(_fromUtf8("actionRunScript"))
        self.actionSave = QtGui.QAction(Form)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.actionNew = QtGui.QAction(Form)
        self.actionNew.setObjectName(_fromUtf8("actionNew"))
        self.actionImportPlugin = QtGui.QAction(Form)
        self.actionImportPlugin.setEnabled(False)
        self.actionImportPlugin.setVisible(False)
        self.actionImportPlugin.setObjectName(_fromUtf8("actionImportPlugin"))
        self.actionExportPlugin = QtGui.QAction(Form)
        self.actionExportPlugin.setObjectName(_fromUtf8("actionExportPlugin"))
        self.actionOpen = QtGui.QAction(Form)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSaveAs)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionImportPlugin)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExportPlugin)
        self.menuRun.addAction(self.actionRunScript)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuRun.menuAction())

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Scripting", None))
        self.menuFile.setTitle(_translate("Form", "File", None))
        self.menuRun.setTitle(_translate("Form", "Run", None))
        self.label_2.setText(_translate("Form", "Output", None))
        self.textEditOutput.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Consolas\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.actionSaveAs.setText(_translate("Form", "Save as ...", None))
        self.actionRunScript.setText(_translate("Form", "Run script", None))
        self.actionRunScript.setShortcut(_translate("Form", "F5", None))
        self.actionSave.setText(_translate("Form", "Save", None))
        self.actionSave.setShortcut(_translate("Form", "Ctrl+S", None))
        self.actionNew.setText(_translate("Form", "New", None))
        self.actionNew.setShortcut(_translate("Form", "Ctrl+N", None))
        self.actionImportPlugin.setText(_translate("Form", "Import plugin", None))
        self.actionExportPlugin.setText(_translate("Form", "Export as plugin", None))
        self.actionOpen.setText(_translate("Form", "Open", None))
        self.actionOpen.setToolTip(_translate("Form", "Open script", None))
        self.actionOpen.setShortcut(_translate("Form", "Ctrl+O", None))

from PyQt4 import QtWebKit

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

