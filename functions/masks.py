'''
Created on 11/12/2014

@author: mmpe
'''
import numpy as np
def constant_values(sig, x=None, include_first=False, unit_reps=1, atol=0):

    rep = np.r_[False, (np.abs(sig[1:] - sig[:-1]) <= atol), False]
    if unit_reps == 1 and x is None and not include_first:
        return rep
    if x is None:
        x = np.arange(len(sig))
    tr = rep[1:] ^ rep[:-1]
    itr = np.where(tr)[0]

    if len(itr) % 2 == 1:
        itr = itr[:-1]

    mask = np.zeros_like(sig).astype(np.bool)
    for start, end, l in zip (itr[::2] , itr[1::2], x[itr[1::2]] - x[itr[::2]]):
        if l >= unit_reps:
            mask[start + 1 - int(include_first) :end + 1] = 1
    return mask

def constant_cyclic_values(sig, x=None, include_first=False, no_rep=1, cycle_len=1, atol=0):
    if x is None:
        x = np.arange(len(sig))
    rep = np.r_[[False] * cycle_len, (np.abs(sig[cycle_len:] - sig[:-cycle_len]) <= atol)]
    if no_rep == 1 and not include_first:
        return rep

    tr = rep[1:] ^ rep[:-1]
    itr = np.where(tr)[0]
    if len(itr) % 2 == 1:
        itr = itr[:-1]

    mask = np.zeros_like(sig).astype(np.bool)
    for start, end, l in zip (itr[::2] , itr[1::2], itr[1::2] - itr[::2]):
        if l >= no_rep:
            mask[start + 1 - cycle_len * int(include_first) :end + 1] = 1
    return mask

def linear_values(sig, include_first=False, no_rep=1, atol=0):
    rep = np.r_[[False, False], (np.abs(np.diff(np.diff(sig))) <= atol)]
    if no_rep == 1 and not include_first:
            return rep

    tr = rep[1:] ^ rep[:-1]
    itr = np.where(tr)[0]
    if len(itr) % 2 == 1:
        if itr[0] == 1:
            itr = itr[:-1]
        else:
            itr = np.r_[itr, len(tr)]

    mask = np.zeros_like(sig).astype(np.bool)
    for start, end, l in zip (itr[::2] , itr[1::2], itr[1::2] - itr[::2]):
        if l >= no_rep - 1:
            mask[start + no_rep - 1 - no_rep * int(include_first) :end + 1] = 1
    return mask

