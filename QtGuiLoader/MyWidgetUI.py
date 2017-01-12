# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\mmpe\QtGuiLoader\MyWidgetUI.ui'
#
# Created: Thu Jan 12 09:08:14 2017
#      by: PyQt4 UI code generator 4.9.6
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
        Form.resize(223, 164)
        self.horizontalLayoutWidget = QtGui.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(9, 9, 191, 25))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lineEdit = QtGui.QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout.addWidget(self.pushButton)
        self.actionPrintText = QtGui.QAction(Form)
        self.actionPrintText.setObjectName(_fromUtf8("actionPrintText"))

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.actionPrintText.trigger)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.lineEdit.setText(_translate("Form", "test", None))
        self.pushButton.setText(_translate("Form", "PushButton", None))
        self.actionPrintText.setText(_translate("Form", "PrintText", None))

