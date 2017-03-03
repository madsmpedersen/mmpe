import os
import sys


def build_exe(filename, version="1.0.0", description="", author="", modules=[], includes=[], packages="[]", include_files=[], zip_includes=[], icon=None, additional_executables=[], gui=True,onefile=False, name=None):
    basename = filename.replace('.py', '')
    args = []
    if onefile: args.append("--onefile")
    if gui: args.append("--noconsole")
    if name: args.append("-n "+name)
    if icon: args.append('-i '+ icon)
        
    cmd = '%s/scripts/pyinstaller.exe %s %s' % (os.path.dirname(sys.executable)," ".join(args), filename)
    print (cmd)
    os.system(cmd)
    print ("finish")