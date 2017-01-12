'''
Created on 11/07/2013

@author: mmpe
'''

import os
import shutil
import unittest

from mmpe.io import make_dirs


nr = 0
class TestMakedir(unittest.TestCase):

    def test_makedir(self):
        path = "myfolder1/myfolder2/myfile.fil"
        shutil.rmtree('myfolder1', ignore_errors=True)
        make_dirs(path)
        self.assertTrue(os.path.isdir("myfolder1/myfolder2/"))
        with open(path, 'w'):
            pass
        self.assertTrue(os.path.isfile(path))

        # repeat and check that file is not deleted
        make_dirs("myfolder1/myfolder2/myfile.fil")
        self.assertTrue(os.path.isdir("myfolder1/myfolder2/"))
        self.assertTrue(os.path.isfile(path))




if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
