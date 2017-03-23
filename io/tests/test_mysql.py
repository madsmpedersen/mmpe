'''
Created on 19/09/2014

@author: MMPE
'''
import unittest
from mmpe.io.mysql import MySqlReader, MySqlWriter
from mmpe.ui.qt_ui import QtInputUI
try:
    import x  # @UnresolvedImport
except: 
    x=None
import multiprocessing
import time

def task(n):
    print("in ", n)
    with MySqlReader(server="10.40.20.10", database="poseidon", username='mmpe', password=x.password) as reader:
        #time.sleep(1)
        pass
    print("out ", n)
class Test(unittest.TestCase):
    pass

#     def testRead_localhost(self):
#         with MySqlReader('localhost', 'world',"mmpe", x.mmpe_sql, 3306) as reader:
#             print (reader.tables())
            
            #print (pd.read_sql('select * from city;', reader.db))

#     def testRead(self):
#         if x:
#             with MySqlReader(server="10.40.20.10", database="poseidon", username='mmpe', password=x.mmpe_sql) as reader:
#                 self.assertTrue("calmeans" in reader.tables())
# 
#     def testRead2(self):
#         if x:
#             reader = MySqlReader(server="10.40.20.10", database="poseidon", username='mmpe', password=x.mmpe_sql)
#             reader.open()
#             self.assertTrue("calmeans" in reader.tables())
#             reader.close()
# 
# 
#     def testPoolRead(self):
#         if x:
#             p = multiprocessing.Pool()
#             p.map_async(task, range(500))
            
#     def testRead3307(self):
#         with MySqlReader('ri-veadbs03', 'hovsore',"mmpe", x.mmpe_sql, 3306) as reader:
#             print (reader.tables())
        
#     def testRead_localhost(self):
#         with MySqlReader('localhost', 'world',"mmpe", x.mmpe_sql, 3306) as reader:
#             print (reader.read("select * from city;"))
#             import pandas as pd
#             #print (pd.read_sql('select * from city;', reader.db))

#    def testShape(self):
#        self.assertEqual(self.reader.shape('channel_names'), (135, 2))
#        self.assertEqual(self.reader.shape('channel_names', where="in_use='T'"), (130, 2))
#        self.assertEqual(self.reader.shape('channel_names', first_row=10, where="in_use='T'"), (120, 2))
#        self.assertEqual(self.reader.shape('channel_names', first_row=10, last_row=30, where="in_use='T'"), (20, 2))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testRead']
    unittest.main()
