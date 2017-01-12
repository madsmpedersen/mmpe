'''
Created on 29/01/2014

@author: MMPE
'''
import unittest
import time
from mmpe.functions.timing import print_time, print_line_time
import sys
from StringIO import StringIO

def get_stdout(func, *args, **kwargs):
    stdout = StringIO()
    sys.stdout = stdout
    func(*args, **kwargs)
    sys.stdout = sys.__stdout__
    stdout.seek(0)
    return stdout.read()


class Test(unittest.TestCase):

    def test_print_time(self):
        self.assertEqual("test        \t0.400s\n", get_stdout(test))

    def test_print_line_time(self):
        test_line()

@print_time
def test():
    time.sleep(.4)


@print_line_time
def test_line():
    time.sleep(.1)
    time.sleep(.2)
    time.sleep(.3)





if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
