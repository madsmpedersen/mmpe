'''
Created on 01/07/2015

@author: MMPE
'''
import unittest
from mmpe.functions import pomap

def func(x):
    return x + 3

class Test(unittest.TestCase):


    def testpomap(self):

        print (list(map(func, range(100))))
        print (pomap(func, range(100)))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testpomap']
    unittest.main()
