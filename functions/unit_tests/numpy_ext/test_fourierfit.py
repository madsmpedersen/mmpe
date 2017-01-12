'''
Created on 29/10/2015

@author: MMPE
'''
import unittest
import numpy as np
from mmpe.functions.numpy_ext.fourier_fit import F2x, x2F, rx2F, rF2x
from pylab import *
from mmpe.functions.geometric import rad

class Test(unittest.TestCase):


    def test_F2x_and_x2F(self):
        A = [(-0.41213343735370372 + 0j), (0.060927059582462348 + 0.044185523469351493j), (-0.0065342827132377056 - 0.0049239144905786148j), (-0.0080120944779910677 + 0.020703700158749467j), (-0.00021267743879381217 + 0.00068950283985000414j), (-0.000487676726976743 - 0.0025354857132147577j), (0.00039798626767393772 + 0.00023906968705974784j), 0j, 0j, 0j, 0j, 0j, 0j]
        np.testing.assert_array_almost_equal(A, x2F(F2x(A), 6))


    def test_rf2x_and_rx2F(self):
        x = F2x([(-0.41213343735370372 + 0j), (0.060927059582462348 + 0.044185523469351493j), (-0.0065342827132377056 - 0.0049239144905786148j), (-0.0080120944779910677 + 0.020703700158749467j), (-0.00021267743879381217 + 0.00068950283985000414j), (-0.000487676726976743 - 0.0025354857132147577j), (0.00039798626767393772 + 0.00023906968705974784j), 0j, 0j, 0j, 0j, 0j, 0j])
        rF = rx2F(x, 7)
        plot(x)
        yaw = np.arange(360)
        theta = rad(yaw)
        plot(np.sum([np.real(rF[i]) * np.cos(i * theta) + np.imag(rF[i]) * np.sin(i * theta) for i in range(len(rF))], 0))
        plot(rF2x(rF))
        show()
        np.testing.assert_array_almost_equal(x, rF2x(rx2F(x, 6)))

#
#    def test_(self):
#        F = np.zeros(7)
#        F[-1] = 1
#        x = np.fft.irfft(F)
#        print (np.fft.fft(x))
#        print
#        print (X)
#        plot(np.fft.irfft(F))
#        legend()
#        show()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_F2x_and_x2F']
    unittest.main()
