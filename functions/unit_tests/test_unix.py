'''
Created on 03/07/2015

@author: MMPE
'''
import unittest
from gtsdf.unix_time import from_unix, from_unix_old
from mmpe.functions.timing import get_time, print_time, print_cum_time, \
    print_line_time
import datetime
import numpy as np
from datetime import date


day_dict = {}


#def ymd(d):
#    global day_dict
#    if d not in day_dict:
#        day_dict[d] = datetime.date.fromordinal(719163 + d).timetuple()[:3]
#    return day_dict[d]

@print_time
def insert_ymd(d):
    global day_dict

@print_time
def ymd(d):
    global day_dict
    return np.array([day_dict[d_] for d_ in d]).T



r = np.arange(0, 10000000, 99, dtype=np.float) + .1

class Test(unittest.TestCase):


    @get_time
    def fu(self, f):
        return [f(i) for i in r][-1]

    @get_time
    def fu2(self):
        return [datetime(2013, 12, 10, 12, 13, i % 60) for i in r][-1]

    @get_time
    def fu3(self, f):
        return f(r)[-1]


    def testUnix1(self):
        print(self.fu(from_unix_old))


    def testUnix2(self):
        print(self.fu3(from_unix))



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testUnix1']
    unittest.main()
