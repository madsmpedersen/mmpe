'''
Created on 11/07/2013

@author: mmpe
'''
import sys
import os
from mmpe.build_exe.cx.tests.demonstration.matplotlibwidget import MatplotlibWidget
if os.path.realpath("../../../") not in sys.path:
    sys.path.append(os.path.realpath("../../../"))
import os

from mmpe.build_exe.cx import  build_cx_exe

import os
import shutil

import unittest
from mmpe.build_exe.cx.build_cx_exe import NUMPY, HDF5, SCIPY, PYQT4, MATPLOTLIB, \
    CTYPES



class Test_exe(unittest.TestCase):




    def test_exe(self):
        if os.path.isdir("my_program_dist"):
            shutil.rmtree("my_program_dist/")
        import pandas

        build_cx_exe.build_exe('my_program.py', "2.0.0", modules=[NUMPY, CTYPES], includes=["pandas"])
        self.assertTrue(os.path.isfile("my_program_dist/exe.win32-2.7/my_program.exe"))



#    def test_pyqt4(self):
#        if os.path.isdir("demonstration/pyqt_window_dist"):
#            shutil.rmtree("demonstration/pyqt_window_dist/")
#        build_cx_exe.build_exe('demonstration/pyqt_window.py', "2.0.0", modules=[PYQT4, MATPLOTLIB, NUMPY], include_files=['DTU_logo.png'])
#        #self.assertTrue(os.path.isfile("demonstration\\pyqt_window_dist\\exe.win-amd64-3.3\\pyqt_window.exe"))
#        #os.system("demonstration\\pyqt_window_dist\\exe.win-amd64-3.3\\pyqt_window.exe")

#    def test_pyqt4_2(self):
#        if os.path.isdir("demonstration/pyqt_window_dist"):
#            shutil.rmtree("demonstration/pyqt_window_dist/")
#        build_cx_exe.build_exe('demonstration/pyqt_window.py', "2.0.0", modules=[PYQT4, MATPLOTLIB, NUMPY], icon='demonstration/pydap.ico')
#        self.assertTrue(os.path.isfile("demonstration\\pyqt_window_dist\\exe.win-amd64-3.3\\pyqt_window.exe"))
#        os.system("demonstration\\pyqt_window_dist\\exe.win-amd64-3.3\\pyqt_window.exe")

#    def test_hdf5_exe(self):
#        if os.path.isdir("my_program_dist"):
#            shutil.rmtree("my_program_dist/")
#        import pandas
#
#        build_cx_exe.build_exe('my_program.py', "2.0.0", modules=[NUMPY, HDF5])
#        self.assertTrue(os.path.isfile("my_program_dist/exe.win-amd64-3.3/my_program.exe"))
#        print ("finish")



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
