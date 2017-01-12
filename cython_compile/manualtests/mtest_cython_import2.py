'''
Created on 11/07/2013

@author: mmpe
'''


import sys
import unittest

from wetb.utils.cython_compile.cython_compile import cython_import, is_compiled


class Test_cython_import(unittest.TestCase):


    def setUp(self):
        sys.path.append(".")

    def test_compiled(self):
        cython_import('peak_trough')
        import peak_trough
        print (is_compiled(peak_trough))

    def test_compiled2(self):
        cython_import('pair_range')
        import pair_range
        print (is_compiled(pair_range))

    def test_compiled3(self):
        cython_import('rainflowcount_astm')
        import rainflowcount_astm
        print (is_compiled(rainflowcount_astm))



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
