'''
Created on 06/09/2013

@author: Mads M. Pedersen (mmpe@dtu.dk)
'''
from mmpe.build_exe.cx.build_cx_exe import NUMPY, PYQT4, MULTIPROCESSING, CTYPES
import os

from mmpe.build_exe.cx import build_cx_exe as build_exe
#from mmpe.build_exe.pyinstaller import build_exe
build_exe.build_exe("controller.py", version="1.0.0", modules=[PYQT4, MULTIPROCESSING, NUMPY, CTYPES],
                       includes=["PyQt4.QtNetwork", "PyQt4.Qsci"],
                       include_files=['docs/doc.html', 'docs/source.html', 'docs/index.html', 'docs/ScriptFunctions.html'],
                       packages=['appfuncs'])
os.system('controller_dist\\exe.win32-2.7\\controller.exe')