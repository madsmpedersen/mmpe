'''
Created on 15/01/2014

@author: MMPE
'''
import unittest

from mmpe.functions.geometric import rad, deg
from mmpe.functions.geometric.euler import *
import numpy as np

npEqual = np.testing.assert_array_equal
npAlmostEqual = np.testing.assert_array_almost_equal
class Test(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)




    def test_euler2angle(self):
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
