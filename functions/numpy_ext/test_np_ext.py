'''
Created on 19/03/2014

@author: mmpe
'''
import unittest

import mmpe.functions.numpy_ext as np_ext
import numpy as np
class Test(unittest.TestCase):


    def test_bin(self):
        bin_x, bin_y, bin_count, bin_edges = np_ext.bin([0, 1, 2, 3, 2, 3], [1, 1, 1, 1, 2, 2], 2)
        np.testing.assert_array_equal(bin_x, [np.mean([0,1]), np.mean([2,3,2,3])])
        self.assertEqual(list(bin_y), [(1 + 1) / 2, (1 + 1 + 2 + 2) / 4])
        self.assertEqual(list(bin_count), [2, 4])
        np.testing.assert_array_almost_equal(bin_edges, [0, 1.5, 3])

    def test_bin_nan(self):
        bin_x, bin_y, bin_count, bin_edges = np_ext.bin([0, 1, 2, 3, 2, 3, 2, np.nan], [1, 1, 1, 1, 2, 2, np.nan, 2], 2)
        np.testing.assert_array_equal(bin_x, [np.mean([0,1]), np.mean([2,3,2,3])])
        self.assertEqual(list(bin_y), [(1 + 1) / 2, (1 + 1 + 2 + 2) / 4])
        self.assertEqual(list(bin_count), [2, 4])
        np.testing.assert_array_almost_equal(bin_edges, [0, 1.5, 3])


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_linalg']
    unittest.main()
