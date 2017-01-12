import os
import sys


def build_exe(filename, version="1.0.0", description="", author="", modules=[], includes=[], packages="[]", include_files=[], zip_includes=[], icon=None, additional_executables=[], target=None):
    basename = filename.replace('.py', '')
    cmd = '%s/scripts/pyinstaller.exe  -F --noconsole %s' % (os.path.dirname(sys.executable), filename)
    print (cmd)
    os.system(cmd)
    print ("finish")