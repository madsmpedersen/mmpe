from cx_Freeze import setup, Executable

try:
    import set_path
    set_path.set_path()
except:
    pass
import os
os.environ['TCL_LIBRARY'] = r"C:\Anaconda3\tcl\tcl8.6"
os.environ['TK_LIBRARY'] = r"C:\Anaconda3\tcl\tk8.6"

build_exe_options = {
"include_msvcr": True,
"includes": ['PyQt4.QtNetwork','PyQt4.Qsci','sip','PyQt4.QtWebKit','PyQt4.QtNetwork','PyQt4.Qsci'],
"packages": ['appfuncs'],
'excludes' : ['PyQt4.uic.port_v3', 'Tkconstants', 'tcl', 'tk', 'doctest', '_gtkagg', '_tkagg', 'bsddb', 'curses', 'email', 'pywin.debugger', 'pywin.debugger.dbgcon', 'pywin.dialogs', 'Tkinter', 'tables', 'zmq', 'win32', 'Pythonwin', 'Cython', 'statmodels', 'cvxopt', '_sqlite3', '_ssl', '_testcapi', 'markupsafe', 'numexpr', '_elementtree', '_hashlib', '_testcapi', 'bz2', 'simplejson', 'pyexpat', 'lxml', 'IPython', 'matplotlib', 'guidata', 'PySide', 'scipy', 'docx', '_opengl', 'PIL', 'h5py'],
"include_files": ['docs/doc.html','docs/source.html','docs/index.html','docs/ScriptFunctions.html','imageformats/',],
"zip_includes": []}

setup(
name = "controller",
version="1.0.0",
description="",
author = "",
options = { "build_exe": build_exe_options},
executables = [Executable("controller.py", base='Win32GUI', shortcutName="controller", shortcutDir="DesktopFolder")])
    