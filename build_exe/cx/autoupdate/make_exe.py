
from mmpe.build_exe.cx.autoupdate import version_app_gui
import imp
import os
from mmpe.build_exe.cx.build_cx_esky_exe import build_esky_exe, PYQT4
with open(version_app_gui.__file__) as fid_in:
    v = version_app_gui.version
    txt = fid_in.read().replace(str(v), "(%d, %d, %d)" % (v[0], v[1], v[2] + 1))

with open(version_app_gui.__file__, 'w') as fid_out:
    fid_out.write(txt)
imp.reload(version_app_gui)
print (version_app_gui.version)
#from mmpe.build_exe.cx.build_cx_exe import build_exe
build_esky_exe('version_app_gui.py', ".".join([str(v) for v in version_app_gui.version]), modules=[PYQT4], include_files=['pydap.ico'], gui_only="False")
#os.system("python setup_gui.py bdist_esky")
print ("finish" + (str(version_app_gui.version)))
