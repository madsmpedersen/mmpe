'''
Created on 11/11/2013

@author: mmpe
'''
import os
import random
import string
import sys
import time
import unittest

from mmpe.algorithms.string_distance import SmartDistance

from mmpe.algorithms.test import score_dict_cython
from mmpe.cython_compile.cython_compile import cython_compile
import numpy as np


sys.path.append("../")
class Test(unittest.TestCase):



    def testStringMatching4(self):
        w = 'Mads'
        a, b, c = ([SmartDistance().get_score(w, l) / len(w) for l in ['mads', 'mdsa', 'mds']])
        self.assertTrue(a < c)
        self.assertTrue(c < b)


#    def testStringMatching2(self):
#        lst = SmartDistance([(u"0", "o", 1)]).score_lst_sorted("Ford", ["Porche", "ford", "opel", "Opel", "Fo rd", "F0rd"], 1, False)
#        self.assertEqual(['F0rd', 'ford', 'Fo rd', 'Porche'], lst)


#    def testStringMatching3(self):
#        s1 = SmartMatch().get_score("b", "aaaaaaba")
#        s2 = SmartMatch().get_score("b    ", "baaaaaa")
#        s3 = SmartMatch().get_score("b", "baaaaaa")
#        self.assertTrue(s1 > 0)
#        self.assertTrue(s2 > 0)
#        print s1, s2, s3
#
#
#    def testMatchingTime(self):
#
#        def random_string(size=6, chars=string.ascii_letters):
#            return ''.join(random.choice(chars) for _ in range(size))
#        lst = [random_string(i) for i in np.random.randint(10, 20, 500)] + ["Mads M. Pedersen"]
#        t = time.time()
#        s = SmartMatch().score_dict("Mads M Pedersen", lst)
#        t1 = time.time() - t
#        #print s
#        t = time.time()
#        from mmpe.cython_compile_depr import cython_import
#        cython_import('string_matching_cython')
#        import string_matching_cython  # import must be after cython_import statement
#        s = string_matching_cython.score_dict("Mads M Pedersen", lst)
#        t2 = time.time() - t
#        #print t2, t1
#        self.assertLess(t2 * 2, t1)
#
#    def testMatchingCython(self):
#        from mmpe.cython_compile_depr import cython_import
#        cython_import('string_matching_cython')
#        import string_matching_cython  # import must be after cython_import statement
#        d = string_matching_cython.generate_special_scores([('D', 'd', 1)])
#        s = string_matching_cython.score_dict("Mads", ["mads", "MaDs"], d)
#        self.assertAlmostEqual(s['mads'], 0.975)
#        self.assertEqual(s['MaDs'], 1)
#
#



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testStringMatching1']
    unittest.main()
