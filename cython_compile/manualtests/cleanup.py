'''
Created on 21/11/2013

@author: mmpe
'''
import os
import sys
import time


def cleanup(folder="."):
    for f in os.listdir():
        _, ext = os.path.splitext(f)
        if ext in ['.c', '.pyx', '.pyd']:
            try:
                os.remove(f)
                print (f)
            except PermissionError:
                pass
if __name__ == "__main__":
    cleanup()
