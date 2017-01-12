'''
Created on 29. sep. 2016

@author: mmpe
'''
import unittest

import mmpe.functions.numpy_ext as np_ext
class Test(unittest.TestCase):


    def testBin(self):
        x = [10.234302313156817, 13.98517783627376, 7.7902362498947921, 11.08597865379001, 8.430623529700588, 12.279982848438033, 33.89151260027775, 12.095047111211629, 13.731371675689642, 14.858309846006723, 15.185588405617654]
        y = [28.515665187174477, 46.285328159179684, 17.763652093098958, 32.949007991536462, 20.788106673177083, 38.819226477864589, 96.53278479817709, 38.479684539388025, 46.072654127604167, 51.875484233398439, 53.379342967122398]
        bin_x, bin_y, bin_count, bin_edges = np_ext.bin(x, y, bins=15)
        print (bin_x, bin_y, bin_count)
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testBin']
    unittest.main()
