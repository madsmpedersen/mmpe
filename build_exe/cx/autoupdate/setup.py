from distutils.core import setup
from esky import bdist_esky
from esky.bdist_esky import Executable


build_exe_options = {
"includes": ['sip','PyQt4.QtWebKit','PyQt4.QtNetwork','PyQt4.Qsci'],
'excludes' : ['PyQt4.uic.port_v3', 'Tkconstants', 'tcl', 'tk', 'doctest', '_gtkagg', '_tkagg', 'bsddb', 'curses', 'pywin.debugger', 'pywin.debugger.dbgcon', 'pywin.dialogs', 'Tkinter', 'tables', 'zmq', 'win32', 'Pythonwin', 'Cython', 'statmodels', 'cvxopt', '_sqlite3', '_ssl', '_testcapi', 'markupsafe', 'numexpr', '_elementtree', '_hashlib', '_testcapi', 'simplejson', 'pyexpat', 'lxml', 'matplotlib', 'guidata', 'PySide', 'scipy', 'numpy', '_multiprocessing', 'docx', '_opengl', 'PIL', 'h5py'],
'freezer_module': "cxfreeze",

}
executable = Executable("version_app_gui.py",  gui_only=False)
setup(
name = "version_app_gui",
version="1.1.56",
description="",
author = "",
scripts = [executable],
data_files = ['pydap.ico'],
script_args = ("bdist_esky",),
options = { "bdist_esky": build_exe_options})
    