'''
Created on 29/01/2014

@author: MMPE
'''
import unittest
from mmpe.functions.deep_coding import deep_encode, to_str, deep_decode


class Test(unittest.TestCase):

    def test_deep_encode(self):
        self.assertEqual(deep_encode(b'hej'), b'hej')

    def test_deep_decode(self):
        self.assertEqual(deep_decode(b'hej'), 'hej')


    def test_to_str(self):
        self.assertEqual(to_str(b'hej'), 'hej')
        self.assertEqual(to_str('hej'), 'hej')

    def test_to_bytes(self):
        self.assertEqual(to_str(b'hej'), 'hej')
        self.assertEqual(to_str('hej'), 'hej')



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
