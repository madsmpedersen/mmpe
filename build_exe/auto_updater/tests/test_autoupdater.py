'''
Created on 8. feb. 2017

@author: mmpe
'''
import os
import shutil
import unittest

from mmpe.build_exe.auto_updater import AutoUpdater

tfp = os.path.dirname(__file__) + "/test_files/"
tmp_dir = tfp + "tmp/"
app_dir = tfp + "test_app_folder/"


def remove_tmp_dir():
    if os.path.isdir(tmp_dir):
        shutil.rmtree(tmp_dir)
        
class Test(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.autoupdater = AutoUpdater('http://tools.windenergy.dtu.dk/test_application/downloads/index.htm', tmp_dir, "test_application")
    
    def testAutoupdater(self):
        self.assertTrue((0,2,0) in self.autoupdater.versions)
        info = self.autoupdater.info((0,2,0))
        self.assertEqual(info['zip'], "test_application_0.2.0_win-amd64.zip")
     
    def test_download_zip(self):
        remove_tmp_dir()
        self.autoupdater._download_zip((0,2,0))
        self.assertTrue(os.path.isfile(tfp + "tmp/test_application/test_application_0.2.0_win-amd64.zip"))
         
    def test_update(self):
        remove_tmp_dir()
        self.autoupdater.update((0,1,0))
        self.assertTrue(os.path.isfile(tfp + "tmp/test_application/test_application_0.1.0_win-amd64/test_application.exe"))
        self.autoupdater.update((0,2,0))
        self.assertTrue(os.path.isfile(tfp + "tmp/test_application/test_application_0.2.0_win-amd64/test_application.exe"))
        self.autoupdater.update((0,3,0))
        self.assertTrue(os.path.isfile(tfp + "tmp/test_application/test_application_0.2.0_win-amd64/test_application.exe"))
        
    def test_get_local_versions(self):
        autoupdater = AutoUpdater('http://tools.windenergy.dtu.dk/test_application/downloads/index.htm', app_dir, "test_application")
        self.assertEqual(autoupdater.get_local_versions()[1]["0.2.0"], "test_application_0.2.0_win-amd64") 
         
        
    def test_check_updates(self):
        remove_tmp_dir()
        self.autoupdater.update((0,1,0))
        def get_confirmation(title, msg):
            print (title)
            print (msg)
            return True 
        self.autoupdater.ui.get_confirmation = get_confirmation
        self.autoupdater.check_for_updates()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testAutoupdater']
    unittest.main()