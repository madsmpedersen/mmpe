
import os
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QMessageBox, QFileDialog, QInputDialog
from mmpe.ui.qt_progress_information import QtProgressInformation
import sys
import traceback
from mmpe.ui import OutputUI, InputUI, StatusUI, UI


class QtOutputUI(OutputUI):
    show_traceback = False






    def _show_box(self, box_func):
        cursor = QtGui.QApplication.overrideCursor()
        QtGui.QApplication.restoreOverrideCursor()
        box_func()
        if cursor and isinstance(cursor, QtGui.QCursor) and cursor.shape() == QtCore.Qt.WaitCursor:
            QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        QtGui.QApplication.processEvents()



    def show_message(self, msg, title="Information"):
        self._show_box(lambda : QMessageBox.information(self.parent, title, msg))

    def show_warning(self, msg, title="Warning"):
        """Show a warning dialog box
        msg: Error message or Warning object
        """
        if isinstance(msg, Warning):
            title = msg.__class__.__name__
            msg = str(msg)

        self._show_box(lambda : QMessageBox.warning(self.parent, title, msg))

    def show_error(self, msg, title="Error"):
        """Show a warning dialog box
        msg: Error message or Exception object
        """
        if isinstance(msg, Exception):
            e = msg
            title = e.__class__.__name__
            msg = str(e)
            if self.show_traceback:
                msg += "\n" + traceback.format_exc()
        self._show_box(lambda : QMessageBox.critical(self.parent, title, msg))

    def show_text(self, text, end="\n", flush=False):
        print (text, end=end)
        if flush:
            sys.stdout.flush()


class QtInputUI(InputUI):
    def __init__(self, parent):
        if QtGui.QApplication.instance() is None:
            self.app = QtGui.QApplication(sys.argv)  # For unit testing
        self.parent = parent

    def get_confirmation(self, title, msg):
        return QMessageBox.Yes == QMessageBox.question(self.parent, title, msg, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

    def get_confirmation_dontaskagain(self, title, msg):
        class DialogWithCheckBox(QMessageBox):
            def __init__(self, parent, title, msg):
                super(DialogWithCheckBox, self).__init__()

                self.checkbox = QtGui.QCheckBox()
                #Access the Layout of the MessageBox to add the Checkbox
                layout = self.layout()
                layout.addWidget(self.checkbox, 1, 2)
                self.setWindowTitle(title)
                self.setText(msg)
                self.checkbox.setText("Remember my decision")
                self.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                self.setDefaultButton(QMessageBox.Yes)
                self.setIcon(QMessageBox.Question)

            def exec_(self, *args, **kwargs):
                """
                Override the exec_ method so you can return the value of the checkbox
                """
                return QMessageBox.exec_(self, *args, **kwargs), self.checkbox.isChecked()
        answer, dontaskagain = DialogWithCheckBox(self.parent, title, msg).exec_()
        return QMessageBox.Yes == answer, dontaskagain

    def get_string(self, title, msg, default=""):
        """
        returns
        -------
        text : str
            String
        ok : boolean
            if ok: True
            if cancel: False

        Examples
        --------
        text, ok = get_string("The Title", "The meassage", "Default value")
        if ok:
            print (text)
        else:
            print ("cancel")
        """
        return QInputDialog.getText(self.parent, title, msg, text=default)

    def get_username(self, msg="Username"):
        username, ok = QtGui.QInputDialog.getText(None, "Enter username", msg)
        if not ok:
            username = ""
        return str(username)


    def get_password(self, msg="Password"):
        password, ok = QtGui.QInputDialog.getText(None, "Enter password", msg, QtGui.QLineEdit.Password)
        if not ok:
            password = ""
        return str(password)


    def get_login(self, username="", title="Log in"):
        login = Login(username, title)
        login.exec_()
        return str(login.textName.text()), str(login.textPass.text())

    def get_hostlogin(self, host="", username="", title="Log in"):
        login = HostLogin(host, username, title)
        login.exec_()
        return str(login.textHost.text()), str(login.textName.text()), str(login.textPass.text())



    def get_open_filename(self, title="Open", filetype_filter="*.*", file_dir=None, selected_filter=None):
        """
        fn = gui.get_open_filename(title="Open", filetype_filter="*.dit1;*dit2;;*.dat", file_dir=".", selected_filter="*.dat")
        if fn == "": return #Cancel
        """
        if file_dir is None:
            file_dir = self._default_dir(file_dir)

        try:
            r = str(QFileDialog.getOpenFileName(self.parent, title, file_dir, filetype_filter, selected_filter))
        except TypeError:
            r = str(QFileDialog.getOpenFileName(self.parent, title, file_dir, filetype_filter))
        if isinstance(r, tuple):
            r = r[0]
        r = r.replace('\\', '/')
        if r != "":
            self.save_setting("default_dir", os.path.dirname(r))
        return r

    def get_save_filename(self, title, filetype_filter, file_dir=None, selected_filter=""):
        """
        fn = gui.get_save_filename(title="title", filetype_filter="*.dit1;*dit2;;*.dat", file_dir=".", selected_filter="*.dat")
        if fn == "": return #cancel
        """
        if file_dir is None:
            file_dir = self._default_dir(str(file_dir))
        filetype_filter = ";;".join((selected_filter, filetype_filter))
        r = str(QFileDialog.getSaveFileName(self.parent, title, file_dir, filetype_filter))
        if isinstance(r, tuple):
            r = r[0]
        r = r.replace('\\', '/')
        if r != "":
            self.save_setting("default_dir", os.path.dirname(r))
        return r

    def _default_dir(self, file_dir):
        if file_dir is None or os.path.dirname(file_dir) == "":
            default_dir = self.load_setting('default_dir', '.')
            if os.path.isdir(default_dir):
                file_dir = default_dir
            else:
                file_dir = ""
        return file_dir

    def get_open_filenames(self, title, filetype_filter="*.*", file_dir=None):
        """
        fn = gui.get_open_filenames(title="title", filetype_filter="*.dit1;*dit2;;*.dat", file_dir=".")
        if fn == []: return #cancel
        """
        if file_dir is None:
            file_dir = self._default_dir(str(file_dir))
        r = QFileDialog.getOpenFileNames(self.parent, title, file_dir, filetype_filter)
        if isinstance(r, tuple):
            r = r[0]
        r = [str(f).replace('\\', '/') for f in r]
        if len(r) > 0:
            self.save_setting("default_dir", os.path.dirname(r[0]))
        return r

    def get_foldername(self, title='Select folder', file_dir=None):
        file_dir = self._default_dir(file_dir)
        r = str(QFileDialog.getExistingDirectory(self.parent, title, file_dir)).replace('\\', '/')
        if os.path.isdir(r):
            self.save_setting("default_dir", r)
        return r

class Login(QtGui.QDialog):
        def __init__(self, username="", title="Log on as"):
            QtGui.QDialog.__init__(self)
            self.setWindowTitle(title)
            self.textName = QtGui.QLineEdit(username, self)
            self.textPass = QtGui.QLineEdit(self)
            self.textPass.setEchoMode(QtGui.QLineEdit.Password)
            self.buttonLogin = QtGui.QPushButton('Login', self)
            self.buttonLogin.clicked.connect(self.accept)
            layout = QtGui.QFormLayout(self)
            layout.addRow(QtGui.QLabel("Username:"), self.textName)
            layout.addRow(QtGui.QLabel("Password:"), self.textPass)
            layout.addWidget(self.buttonLogin)

class HostLogin(QtGui.QDialog):
        def __init__(self, host="", username="", title='Host connection'):
            QtGui.QDialog.__init__(self)
            self.setWindowTitle(title)
            self.textHost = QtGui.QLineEdit(host, self)
            self.textName = QtGui.QLineEdit(username, self)
            self.textPass = QtGui.QLineEdit(self)
            self.textPass.setEchoMode(QtGui.QLineEdit.Password)
            self.buttonLogin = QtGui.QPushButton('Login', self)
            self.buttonLogin.clicked.connect(self.accept)
            layout = QtGui.QFormLayout(self)
            layout.addRow(QtGui.QLabel("Host:"), self.textHost)
            layout.addRow(QtGui.QLabel("Username:"), self.textName)
            layout.addRow(QtGui.QLabel("Password:"), self.textPass)
            layout.addWidget(self.buttonLogin)





class QtStatusUI(QtProgressInformation, StatusUI):

    def __init__(self, parent):
        QtProgressInformation.__init__(self, parent)
        pass

    def start_wait(self):
        """Changes mouse icon to waitcursor"""
        StatusUI.start_wait(self)
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

    def end_wait(self):
        """Restores default mouse icon"""
        StatusUI.end_wait(self)
        QtGui.QApplication.restoreOverrideCursor()



class QtUI(QtOutputUI, QtInputUI, QtStatusUI, UI):
    def __init__(self, parent):
        QtStatusUI.__init__(self, parent)
        QtInputUI.__init__(self, parent)
        QtOutputUI.__init__(self, parent)


if __name__ == "__main__":
    class MW(QtGui.QMainWindow, QtUI):
        def __init__(self, *args, **kwargs):
            QtGui.QMainWindow.__init__(self, *args, **kwargs)
            QtUI.__init__(self, self)

    app = QtGui.QApplication(sys.argv)
    mw = MW()


    print (mw.get_confirmation_dontaskagain("title", "msg"))

    sys.exit(app.exec_())
