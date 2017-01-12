'''
Created on 24/07/2014

@author: MMPE
'''
import numpy as np

from wetb.utils.timing import print_cum_time


#@cython_compile
def read_fixed_float(filename, column, column_width=13):
    """Slower if compiled"""
    import os
    #cdef int fs, i, lw, offset
    #cdef np.ndarray[np.float64_t, ndim=1] data
    fs = os.path.getsize(filename)
    with open(filename, 'rb') as fid:
        first_line = fid.readline()
        lw = len(first_line)
        if lw == 0:
            raise ValueError("First line of %s must be non-empty" % filename)
        first_value_offset = max(lw - len(first_line.lstrip()) - 1, 0)
        fid.seek(first_value_offset + column_width * column)
        offset = lw - column_width
        data = []
        for _ in range(fs // lw):
            data.append(float(fid.read(column_width)))
            fid.seek(offset, 1)
        return np.array(data)



