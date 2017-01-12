'''
Created on 29/01/2014

@author: MMPE
'''
import unittest
import time
from mmpe.functions.timing import print_time, print_line_time
import sys
from mmpe.functions.optimization import linear, bisect







class Test(unittest.TestCase):

    def test_linear1(self):
        self.assertAlmostEqual(linear.minimize(lambda x : .5 * x - 3, [0, 10], max_iter=100, tolerance=0.00000001, verbose=True)[0][0], 6)


    def test_bisect(self):
        self.assertAlmostEqual(bisect.minimize(lambda x : .5 * x - 3, [0, 10], max_iter=100, tolerance=0.00000001, verbose=True)[0][0], 6)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
