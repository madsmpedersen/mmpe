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
"includes": ['pandas'],
"packages": [],
'excludes' : ['PyQt4.uic.port_v3', 'Tkconstants', 'tcl', 'tk', 'doctest', '_gtkagg', '_tkagg', 'bsddb', 'curses', 'email', 'pywin.debugger', 'pywin.debugger.dbgcon', 'pywin.dialogs', 'Tkinter', 'tables', 'zmq', 'win32', 'Pythonwin', 'Cython', 'statmodels', 'cvxopt', '_sqlite3', '_ssl', '_testcapi', 'markupsafe', 'numexpr', '_elementtree', '_hashlib', '_testcapi', 'bz2', 'simplejson', 'pyexpat', 'lxml', 'IPython', 'matplotlib', 'guidata', 'PyQt4', 'PySide', 'scipy', '_multiprocessing', 'docx', '_opengl', 'PIL', 'h5py'],
"include_files": ['C:/Anaconda3/Library/bin/cilkrts20.dll','C:/Anaconda3/Library/bin/ifdlg100.dll','C:/Anaconda3/Library/bin/libchkp.dll','C:/Anaconda3/Library/bin/libicaf.dll','C:/Anaconda3/Library/bin/libifcoremd.dll','C:/Anaconda3/Library/bin/libifcoremdd.dll','C:/Anaconda3/Library/bin/libifcorert.dll','C:/Anaconda3/Library/bin/libifcorertd.dll','C:/Anaconda3/Library/bin/libifportmd.dll','C:/Anaconda3/Library/bin/libimalloc.dll','C:/Anaconda3/Library/bin/libiomp5md.dll','C:/Anaconda3/Library/bin/libiompstubs5md.dll','C:/Anaconda3/Library/bin/libmmd.dll','C:/Anaconda3/Library/bin/libmmdd.dll','C:/Anaconda3/Library/bin/libmpx.dll','C:/Anaconda3/Library/bin/liboffload.dll','C:/Anaconda3/Library/bin/mkl_avx.dll','C:/Anaconda3/Library/bin/mkl_avx2.dll','C:/Anaconda3/Library/bin/mkl_avx512.dll','C:/Anaconda3/Library/bin/mkl_core.dll','C:/Anaconda3/Library/bin/mkl_def.dll','C:/Anaconda3/Library/bin/mkl_intel_thread.dll','C:/Anaconda3/Library/bin/mkl_mc.dll','C:/Anaconda3/Library/bin/mkl_mc3.dll','C:/Anaconda3/Library/bin/mkl_msg.dll','C:/Anaconda3/Library/bin/mkl_rt.dll','C:/Anaconda3/Library/bin/mkl_sequential.dll','C:/Anaconda3/Library/bin/mkl_tbb_thread.dll','C:/Anaconda3/Library/bin/mkl_vml_avx.dll','C:/Anaconda3/Library/bin/mkl_vml_avx2.dll','C:/Anaconda3/Library/bin/mkl_vml_avx512.dll','C:/Anaconda3/Library/bin/mkl_vml_cmpt.dll','C:/Anaconda3/Library/bin/mkl_vml_def.dll','C:/Anaconda3/Library/bin/mkl_vml_mc.dll','C:/Anaconda3/Library/bin/mkl_vml_mc2.dll','C:/Anaconda3/Library/bin/mkl_vml_mc3.dll','C:/Anaconda3/Library/bin/svml_dispmd.dll',],
"zip_includes": []}

setup(
name = "my_program",
version="2.0.0",
description="",
author = "",
options = { "build_exe": build_exe_options},
executables = [Executable("my_program.py", shortcutName="my_program", shortcutDir="DesktopFolder")])
    