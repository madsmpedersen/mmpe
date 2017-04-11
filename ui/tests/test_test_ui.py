'''
Created on 6. apr. 2017

@author: mmpe
'''
import unittest
from mmpe.ui.text_ui import TextStatusUI
import time
import multiprocessing

def t(i):
    TextStatusUI().show_text(str(i))
    
class Test(unittest.TestCase):


    def testProgresCallBack(self):
        if 0:
            def task(callback):
                for i in range(100):
                    callback(i,100)
                    time.sleep(0.05)
                    
            task (TextStatusUI().progress_callback())
        
    def testProgressIterator(self):
        if 0:
            pool = multiprocessing.Pool(2)
            
            for i in TextStatusUI().progress_iterator(range(100)):
                    time.sleep(0.01)
                    if i%50==0:
                        pool.apply(t,(i,))
                        
        



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()