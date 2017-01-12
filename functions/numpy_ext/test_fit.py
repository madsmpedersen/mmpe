'''
Created on 07/07/2015

@author: MMPE
'''
import unittest
from mmpe.functions.numpy_ext.fit import fourier_fit
import numpy as np
from mmpe.functions.geometric import deg


class Test(unittest.TestCase):


    def test_fourier_fit(self):
        from numpy import nan
        import matplotlib.pyplot as plt
        y = [nan, nan, nan, nan, -0.36773350834846497, -0.34342807531356812, -0.3105124831199646, -0.2949407696723938, nan, nan, nan, nan, nan, nan, nan, nan, -0.37076538801193237, -0.35946175456047058, -0.35366204380989075, -0.34812772274017334, -0.32674536108970642, -0.31197881698608398, -0.31780806183815002, -0.31430944800376892, -0.32355087995529175, -0.35628914833068848, -0.39329639077186584, -0.46684062480926514, -0.48477476835250854, -0.50368523597717285, -0.51693356037139893, -0.50966787338256836, -0.49876394867897034, -0.486896812915802, -0.48280572891235352, -0.4708983302116394, -0.46562659740447998, -0.4582551121711731, -0.46219301223754883, -0.46569514274597168, -0.4741971492767334, -0.48431938886642456, -0.49597686529159546, -0.50340372323989868, -0.50065416097640991]
        #y = [-0.36884582, -0.36256081, -0.35047901, -0.33841938, -0.3289246, -0.32291612, -0.32149044, -0.32851833, -0.34011644, -0.35467893, -0.36627313, -0.37245053, -0.37924927, -0.39883283, -0.38590872, -0.39833149, -0.40406495, -0.4102158, -0.41886991, -0.42862922, -0.43947089, -0.45299602, -0.46831554, -0.48249167, -0.49108803, -0.500368, -0.50779951, -0.51360059, -0.51370221, -0.50541216, -0.49272588, -0.47430229, -0.45657015, -0.44043627, -0.4286592, -0.41741648, -0.41344571, -0.40986174, -0.40896985, -0.40939313, -0.40635225, -0.40435526, -0.40015101, -0.39243227, -0.38454708]
        print (len(y))
        x = np.linspace(0, 360, len(y) + 1)[:len(y)]
        #plt.plot(, y)
        plt.plot(x, y)
        x_fit = fourier_fit.fit_old(y, 5)
        plt.plot(x, x_fit, label='fit2')
        x_fit = fourier_fit.fit(y, 5)
        plt.plot(x_fit, label='fit')

        plt.legend()
        plt.show()

    def test_fourier_fit2(self):
        import matplotlib.pyplot as plt
        t = np.linspace(0, 2 * np.pi, 9 + 1)[:-1]
        y = np.cos(t) + np.sin(t) + 1
        nfft = 4
        print (fourier_fit.x2F(y, nfft))
        plt.plot(deg(t), y, label='cos')
        plt.plot(fourier_fit.fit(y, nfft), label='fit')
        plt.plot(fourier_fit.F2x(np.fft.fft(y) / len(y)), label='fft')
        plt.legend()
        plt.show()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

