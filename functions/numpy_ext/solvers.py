'''
Created on 19/03/2014

@author: mmpe
'''
from numpy import linalg
import numpy as np


def linalg_solve(A, b):
    return linalg.solve(A, b)


def iterative(A, b, x=None, decimal=7, max_iterations=1000):
    I = np.eye(A.shape[0])
    D = I * A
    Di = np.zeros_like(I)
    np.fill_diagonal(Di, 1. / np.diag(D))
    LU = A - D
    B = np.dot(-Di, LU)
    b_ = np.dot(Di, b)
    if x is None:
        x = np.zeros_like(b)
    last = np.ones_like(x) * 999999
    last_diff = np.max(last) * 2
    precision = 10 ** -decimal
    for i in range(max_iterations):
        x = np.dot(B, x) + b_
        diff = np.max(np.abs(x - last))
        print (i, diff, x)
        if diff <= precision:
            return x
        #if diff > last_diff:
        #    raise ValueError("Does not converge")
        last = x
        last_diff = diff
    raise ValueError("Max iterations exceeded. Diff = %f" % diff)


def bisect(func, bounds):
    values = [func(b) for b in bounds]



