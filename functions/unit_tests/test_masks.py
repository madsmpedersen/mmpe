'''
Created on 11/12/2014

@author: mmpe
'''
import unittest
import numpy as np
from mmpe.functions import masks
nan = np.nan
class Test(unittest.TestCase):


    def test_repeated_time(self):
        data = np.array([1., 2, 2, 3, 4, 5, 5, 5, 5, 4, 3, 2, 2, 2, 1])
        time = np.arange(len(data))
        time[2:] += 10
        data[masks.constant_values(data, x=time, unit_reps=5)] = np.nan
        np.testing.assert_array_equal(data, [1.0, 2.0, nan, 3.0, 4.0, 5.0, 5, 5, 5, 4.0, 3.0, 2.0, 2, 2, 1.0])


    def test_repeated(self):
        data = np.array([1., 2, 2, 3, 4, 5, 5, 5, 5, 4, 3, 2, 2, 2, 1])
        data[masks.constant_values(data)] = np.nan
        np.testing.assert_array_equal(data, [1.0, 2.0, nan, 3.0, 4.0, 5.0, nan, nan, nan, 4.0, 3.0, 2.0, nan, nan, 1.0])

    def test_repeated1(self):
        data = np.array([1., 2, 2, 3, 4, 5, 5, 5, 5, 4, 3, 2, 2, 2, 1])
        data[masks.constant_values(data, include_first=True)] = np.nan
        np.testing.assert_array_equal(data, [1.0, nan, nan, 3.0, 4.0, nan, nan, nan, nan, 4.0, 3.0, nan, nan, nan, 1.0])



    def test_repeated2(self):
        data = np.array([1., 2, 2, 3, 4, 5, 5, 5, 5, 4, 3, 2, 2, 2, 1])
        data[masks.constant_values(data, unit_reps=2)] = np.nan
        np.testing.assert_array_equal(data, [1.0, 2.0, 2, 3.0, 4.0, 5.0, nan, nan, nan, 4.0, 3.0, 2.0, nan, nan, 1.0])

    def test_repeated3(self):
        data = np.array([1., 2, 2, 3, 4, 5, 5, 5, 5, 4, 3, 2, 2, 2, 1])
        data[masks.constant_values(data, unit_reps=2, include_first=True)] = np.nan
        np.testing.assert_array_equal(data, [1.0, 2.0, 2, 3.0, 4.0, nan, nan, nan, nan, 4.0, 3.0, nan, nan, nan, 1.0])


    def test_repeated4(self):
        data = np.array([1., 1, 1, 3, 4, 5, 5, 5, 5, 4, 3, 2, 2, 2, 1])
        data[masks.constant_values(data, unit_reps=2, include_first=True)] = np.nan
        np.testing.assert_array_equal(data, [nan, nan, nan, 3, 4, nan, nan, nan, nan, 4, 3, nan, nan, nan, 1])

    def test_repeated_last(self):
        data = np.array([1., 1, 2, 3, 4, 5, 5, 5, 5, 4, 3, 2, 2, 2, 2])
        data[masks.constant_values(data, x=np.arange(len(data)))] = np.nan
        np.testing.assert_array_equal(data, [1.0, nan, 2, 3.0, 4.0, 5.0, nan, nan, nan, 4.0, 3.0, 2.0, nan, nan, nan])



    def test_cycle(self):
        data = np.array([1., 2, 2, 3, 4, 5, 3, 4, 5, 4, 3, 2, 2, 3, 2, 1])
        data[masks.constant_cyclic_values(data, cycle_len=3, include_first=False)] = np.nan
        np.testing.assert_array_equal(data, [1., 2, 2, 3, 4, 5, nan, nan, nan, 4, 3, 2, 2, nan, nan, 1])

    def test_cycle2(self):
        data = np.array([1., 2, 2, 3, 4, 5, 3, 4, 5, 4, 3, 2, 2, 3, 2, 1])
        data[masks.constant_cyclic_values(data, cycle_len=3, no_rep=3, include_first=False)] = np.nan
        np.testing.assert_array_equal(data, [1., 2, 2, 3, 4, 5, nan, nan, nan, 4, 3, 2, 2, 3, 2, 1])

    def test_cycle3(self):
        data = np.array([1., 2, 2, 3, 4, 5, 3, 4, 5, 4, 3, 2, 2, 3, 2, 1])
        data[masks.constant_cyclic_values(data, cycle_len=3, no_rep=3, include_first=True)] = np.nan
        np.testing.assert_array_equal(data, [1., 2, 2, nan, nan, nan, nan, nan, nan, 4, 3, 2, 2, 3, 2, 1])


    def test_linear(self):
        data = np.array([1., 2, 2, 3, 4, 5, 3, 5, 7, 9, 3, 2, 2, 3, 2, 1])
        data[masks.linear_values(data)] = np.nan
        np.testing.assert_array_equal(data, [1., 2, 2, 3, nan, nan, 3, 5, nan, nan, 3, 2, 2, 3, 2, nan])

    def test_linear2(self):
        data = np.array([1., 2, 2, 3, 4.1, 5, 3, 5, 7, 9, 3, 2, 2, 3, 2, 1])
        data[masks.linear_values(data, atol=.2)] = np.nan
        np.testing.assert_array_equal(data, [1., 2, 2, 3, nan, nan, 3, 5, nan, nan, 3, 2, 2, 3, 2, nan])

    def test_linear3(self):
        data = np.array([1., 1, 2, 3, 4, 5, 4, 3, 5, 7, 9, 3, 2, 2, 3, 2, 1])
        data[masks.linear_values(data, no_rep=3)] = np.nan
        np.testing.assert_array_equal(data, [1., 1, 2, 3, nan, nan, 4, 3, 5, 7, nan, 3, 2, 2, 3, 2, 1])

    def test_linear4(self):
        data = np.array([1., 1, 2, 3, 4, 5, 5, 3, 5, 7, 9, 3, 2, 2, 3, 2, 1])
        data[masks.linear_values(data, no_rep=2)] = np.nan
        np.testing.assert_array_equal(data, [1., 1, 2, nan, nan, nan, 5, 3, 5, nan, nan, 3, 2, 2, 3, 2, nan])

#data = np.array([1,1., 2, 2, 3, 4, 5, 5, 5, 5, 4, 3, 2, 2, 2, 1])


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_repeated']
    unittest.main()
