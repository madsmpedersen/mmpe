'''
Created on 08/11/2013

@author: mmpe
'''
import unittest

from mmpe.datastructures.dual_key_dict import DualKeyDict
from mmpe.datastructures.Singleton import singleton

@singleton
class A(object):
    pass

class B(object):
    pass

class Test(unittest.TestCase):

    def setUp(self):
        pass

    def test_singleton(self):
        self.assertEqual(A(), A())
        self.assertNotEqual(B(), B())


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
