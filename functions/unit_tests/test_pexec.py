'''
Created on 29/01/2014

@author: MMPE
'''
import os
os.chdir("../../")
import unittest
import time
from mmpe.functions.timing import print_time, print_line_time
import sys
from io import StringIO
from mmpe.functions import pexec





class Test(unittest.TestCase):

    def test_pexec1(self):
        ret, out, err, cmd = pexec('d')
        self.assertEqual(ret, 1)
        self.assertEqual(out, "")
        self.assertEqual(err, "'d' is not recognized as an internal or external command,\r\noperable program or batch file.\r\n")

    def test_pexec2(self):
        ret, out, err, _ = pexec('dir')
        self.assertEqual(ret, 0)
        o = " Volume in drive C is Default\r\n Volume Serial Number is "
        self.assertEqual(out[:len(o)], o)
        self.assertEqual(err, "")


#    def test_pexec3(self):
#        for path in [r'C:\program files (x86)/notepad++', 'C://program files (x86)/notepad++', r'C:\\program files (x86)/notepad++']:
#            ret, out, err, cmd = pexec(b'cd %s' % path)
#            print(cmd)
#            self.assertEqual(ret, 0, cmd)
#            self.assertEqual(out, "", cmd)
#            self.assertEqual(err, "", cmd)


    def test_pexec4(self):


        #for path in [r'C:\program files (x86)/notepad++', 'C://program files (x86)/notepad++', r'C:\\program files (x86)/notepad++']:
        path = 'c:\\program files (x86)/notepad++.exe'
        ret, out, err, cmd = pexec([path])
        #print (ret)
        #print (out)
        #print (cmd)
        sys.stderr.write(err)
        self.assertEqual(ret, 0, path)
        self.assertEqual(out, "", path)
        self.assertEqual(err, "", path)





if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
