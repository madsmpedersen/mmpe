import os
import sys


def build_exe(filename, version="1.0.0", description="", author="", modules=[], includes=[], packages="[]", include_files=[], zip_includes=[], icon=None, additional_executables=[], target=None, 
              window=True, onefile=True):
    args = []
    if window:
        args.append("--noconsole")
    if onefile:
        args.append("--onefile")
    if hasattr(filename, "__file__"):
        filename = filename.__file__
    cmd = '%s/scripts/pyinstaller.exe %s %s' % (os.path.dirname(sys.executable), " ".join(args), filename)
    print (cmd)
    os.system(cmd)
    print ("finish")
    