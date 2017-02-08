'''
Created on 29/01/2014

@author: MMPE
'''
import os
import unittest
from mmpe.functions import class_list, argument_string
import numpy as np


os.chdir("../../")

class Test(unittest.TestCase):

    def test_class_list(self):
        lst = [cls.__name__ for cls in class_list("algorithms", object)]
        for cls in ['Score', 'IgnoreCaseMatch', 'StringMatch', 'SmartMatch', 'SimpleMatch', 'Score', 'SimpleMatch', 'StringMatch', 'Score', 'SmartMatch', 'IgnoreCaseMatch', 'SmartMatch']:
            self.assertTrue(cls in lst)

    def test_argument_string(self):
        self.assertEqual(argument_string(np.interp), "(x, xp, fp, left=None, right=None, period=None)")




if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
