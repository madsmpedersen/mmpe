'''
Created on 06/09/2013

@author: Mads M. Pedersen (mmpe@dtu.dk)
'''
import time
import sys
import traceback
import numpy


while 1:
    input_str = input(">> ")
    if input_str == "quit()": break
    if input_str == "": input_str = "import h5py"
    try:
        t = time.time()
        _return_ = None
        if input_str.strip().startswith("import") or input_str.strip().startswith("from"):
            exec(input_str, globals(), locals())
        else:
            exec("print (%s)" % input_str, globals(), locals())
        print ("%f" % (time.time() - t))
    except Exception as e:
        print (str(e))
        print (traceback.format_exc())
