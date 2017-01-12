'''
Created on 11/07/2013

@author: mmpe
'''

import inspect
import os
import unittest
from mmpe.build_exe.cx import build_cx_exe



class Test_exe(unittest.TestCase):

    def test_setup(self):
        build_cx_exe.write_setup("name", "version", "description", "author")


        x = ["from cx_Freeze import setup, Executable",
         "",
         "",
         "build_exe_options = {",
         '"includes": [],',
         '"packages": [],',
         "'excludes' : ['PyQt4.uic.port_v3', 'Tkconstants','tcl', 'tk', 'doctest','pdb', 'MSVCP90.dll'],",
         '"include_files": []}',
         '',
         'setup(',
         'name = "name",',
         'version="version",',
         'description="description",',
         'author = "author",',
         'options = { "build_exe": build_exe_options},',
         'executables = [Executable("name.py", shortcutName="name", shortcutDir="DesktopFolder")])']
        with open('setup.py') as fid:
            lines = fid.readlines()
        for l1, l2 in zip(lines, x):
            self.assertEqual(l1.strip(), l2)


    def test_setup_matplotlib(self):
        build_cx_exe.write_setup("name", "version", "description", "author", modules=[build_cx_exe.MATPLOTLIB])
        with open('setup.py') as fid:
            lines = fid.readlines()

        #print "".join(lines)

        self.assertEqual(lines[1].strip(), "import matplotlib")
        self.assertEqual(lines[7].strip(), """"include_files": [( matplotlib.get_data_path(),"mpl-data")]}""")



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
