# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\mmpe\build_exe\cx\tests\demonstration\PlotUI.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.mplcontainer = QtWidgets.QGridLayout()
        self.mplcontainer.setObjectName("mplcontainer")
        self.horizontalLayout.addLayout(self.mplcontainer)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.labelimage = QtWidgets.QLabel(Form)
        self.labelimage.setObjectName("labelimage")
        self.verticalLayout.addWidget(self.labelimage)
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.horizontalLayout.setStretch(0, 3)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.actionUpdate = QtWidgets.QAction(Form)
        self.actionUpdate.setObjectName("actionUpdate")

        self.retranslateUi(Form)
        self.lineEdit.editingFinished.connect(self.actionUpdate.trigger)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.labelimage.setText(_translate("Form", "TextLabel"))
        self.actionUpdate.setText(_translate("Form", "update"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

