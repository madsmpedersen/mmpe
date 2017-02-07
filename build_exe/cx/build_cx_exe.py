'''
Created on 21/01/2013

@author: Mads
'''

import numpy as np
import glob
import os
import shutil
import sys
import time
import zipfile
from mmpe.io import make_dirs, make_packages
NUMPY = 'numpy'
MATPLOTLIB = 'matplotlib'
GUIDATA = 'guidata'
PYQT4 = 'PyQt4'
PYQT4LIM = 'PyQt4Lim'
PYQT5 = "PyQt5"
PYSIDE = 'PySide'
SCIPY = 'scipy'
CTYPES = '_ctypes'
MULTIPROCESSING = '_multiprocessing'
DOCX = "docx"
OPENGL = "_opengl"
PIL = "PIL"
HDF5 = "h5py"
PANDAS = 'pandas'
MMPE = "mmpe"
PARAMIKO = "paramiko"
def build_exe(filename, version="1.0.0", description="", author="", modules=[], includes=[], packages="[]", include_files=[], zip_includes=[], icon=None, additional_executables=[], target=None):
    basename = filename.replace('.py', '')
    if target is None:
        target = '%s_dist/' % basename
    prepare(modules)
    write_setup(basename, version, description, author, modules, includes, packages, include_files, zip_includes, icon, additional_executables)

    shutil.rmtree(target, ignore_errors=True)

    os.system('%s setup.py build' % sys.executable)
    py_ver = "%d.%d" % (sys.version_info[:2])
    if GUIDATA in modules and not os.path.isdir("build/exe.win-amd64-%s/guidata" % py_ver):
        shutil.copytree('guidata/', "build/exe.win-amd64-%s/guidata/" % py_ver)
    shutil.move('./build/', target)

    #os.remove('setup.py')
    clean(modules)

    print ("distribution created (%s/)" % target)

def build_msi(filename, version, description="", author=""):
    basename = filename.replace('.py', '')
    folder = '%s_dist/' % basename
    if os.path.exists(folder):
        shutil.rmtree(folder)
    write_setup(basename, version, description, author)
    os.system('python setup.py bdist_msi')

    shutil.move('./dist/', '%s/' % folder)

    os.remove('setup.py')
    shutil.rmtree('build')
    shutil.rmtree('dist')

    print ("Installer created (%s/)" % (folder))


def write_setup(name, version, description="", author="", modules=[NUMPY], includes=[], packages="[]", include_files=[], zip_includes=[], icon=None, additional_executables=[]):
    """['appfuncs','gui_test']"""
    """["graphics/", "imageformats/", ]"""
    """"includes":["sip"],"""
    imports = []
    base = ""
    excludes = ['PyQt4.uic.port_v3', 'Tkconstants', 'tcl', 'tk', 'doctest', '_gtkagg', '_tkagg', 'bsddb',
                'curses', 'email', 'pywin.debugger', 'pywin.debugger.dbgcon', 'pywin.dialogs', 'Tkinter',
                'tables', 'zmq', 'win32', 'Pythonwin', 'Cython', 'statmodels', 'cvxopt', '_sqlite3', '_ssl', '_testcapi',
                'markupsafe', 'numexpr', '_elementtree', '_hashlib', '_testcapi', 'bz2', 'simplejson', 'pyexpat', "lxml", 'IPython',
                MATPLOTLIB, GUIDATA, PYQT4, PYSIDE, SCIPY, NUMPY, MULTIPROCESSING, CTYPES, DOCX, OPENGL, PIL, HDF5]

    def add(module):
        try:
            excludes.remove(module)
        except:
            pass
    #'pandas', '_socket', 'sip',

    if NUMPY in modules:
        if "Anaconda3" in sys.executable:
            include_files.extend(["C:/Anaconda3/Library/bin/%s" % f for f in ["cilkrts20.dll", "ifdlg100.dll", "libchkp.dll", "libicaf.dll", "libifcoremd.dll", "libifcoremdd.dll", "libifcorert.dll", "libifcorertd.dll", "libifportmd.dll", "libimalloc.dll", "libiomp5md.dll", "libiompstubs5md.dll", "libmmd.dll", "libmmdd.dll", "libmpx.dll", "liboffload.dll", "mkl_avx.dll", "mkl_avx2.dll", "mkl_avx512.dll", "mkl_core.dll", "mkl_def.dll", "mkl_intel_thread.dll", "mkl_mc.dll", "mkl_mc3.dll", "mkl_msg.dll", "mkl_rt.dll", "mkl_sequential.dll", "mkl_tbb_thread.dll", "mkl_vml_avx.dll", "mkl_vml_avx2.dll", "mkl_vml_avx512.dll", "mkl_vml_cmpt.dll", "mkl_vml_def.dll", "mkl_vml_mc.dll", "mkl_vml_mc2.dll", "mkl_vml_mc3.dll", "svml_dispmd.dll"] ])

    if MATPLOTLIB in modules:
        include_files.append("""(matplotlib.get_data_path(),"mpl-data")""")
        imports.append("import matplotlib")
        excludes.remove('email')  #py3_64
        excludes.remove(CTYPES)

    if GUIDATA in modules:
        include_files.append("guidata/images/")
        includes.append("PyQt4.uic.port_v3")

    if PYQT4LIM in modules:
        include_files.append("imageformats/")
        excludes.remove(PYQT4)
        includes.append("sip")
        includes.append(PYQT4)

    if PYQT4 in modules:
        include_files.append("imageformats/")
        includes.append("sip")
        includes.append("PyQt4.QtWebKit")
        includes.append("PyQt4.QtNetwork")
        includes.append("PyQt4.Qsci")
#        includes.append("PyQt4.uic")
#        includes.append("PyQt4.uic.port_v3")
        if os.name == "nt":
            base = "base='Win32GUI', "
        else:
            base = ""

    if PYQT5 in modules:
        pass
        #include_files.append(os.path.dirname(sys.executable) + '/Lib\site-packages\PyQt5\Qt/plugins\platforms\qwindows.dll')
#    if SCIPY in modules:
#        imports.append("import scipy.sparse.csgraph")
#        includes.extend(["scipy.sparse.csgraph._validation",  #"scipy.sparse.linalg.dsolve.umfpack",
#        "scipy.integrate.vode", "scipy.integrate._ode", "scipy.integrate.lsoda"])
#        includes.append("scipy.special._ufuncs_cxx")  #py3_64
#        try:
#            from scipy.sparse.sparsetools import csr, csc, coo, dia, bsr, csgraph
#
#            for f in [csr._csr.__file__,
#                      csc._csc.__file__,
#                      coo._coo.__file__,
#                      dia._dia.__file__,
#                      bsr._bsr.__file__,
#                      csgraph._csgraph.__file__]:
#                shutil.copy(f, os.path.basename(f))
#                include_files.append("%s" % os.path.basename(f))
#        except ImportError:
#            pass
    if DOCX in modules:
        include_files.append("mmpe/docx_document/docx-template_clean/")
        #include_files.append("functions/docx_document/inkscape/")
        includes.append("lxml._elementpath")
        excludes.remove("lxml")
        excludes.remove(PIL)

    if OPENGL in modules:
        includes.append("OpenGL")
        includes.append("OpenGL.platform.win32")
        includes.append("OpenGL.arrays.numpymodule")
        includes.append("OpenGL.arrays.arraydatatype")
        includes.append("OpenGL.converters")
        includes.append("OpenGL.arrays.numbers")
        includes.append("OpenGL.arrays.strings")


    if HDF5 in modules:
        import platform
        if platform.architecture()[0] == "32bit":
            from h5py import _conv, _errors, _objects, _proxy, defs, h5, h5a, h5d, h5ds, h5f, h5fd, h5g, h5i, h5l, h5o, h5p, h5r, h5s, h5t, h5z, utils
            for f in [_conv, _errors, _objects, _proxy, defs, h5, h5a, h5d, h5ds, h5f, h5fd, h5g, h5i, h5l, h5o, h5p, h5r, h5s, h5t, h5z, utils]:
                f = f.__file__
                shutil.copy(f, "h5py." + os.path.basename(f))
                include_files.append("h5py.%s" % os.path.basename(f))
            import h5py
            #for f in [f for f in os.listdir(os.path.dirname(h5py.__file__)) if f.endswith(".pyd")]:
            #    shutil.copy2(os.path.join(os.listdir(os.path.dirname(h5py.__file__)), "h5py.%s" % f))
            #shutil.rmtree("h5py", ignore_errors=True)
            #shutil.copytree(os.path.dirname(h5py.__file__), "h5py")

        else:

            includes.append("h5py")
            includes.append('h5py.h5ac')

        #includes.extend(["'h5py.defs'", "'h5py.utils'", "'h5py._proxy'"])

        pass

    if PANDAS in modules:
        add('email')
        includes.append("Pandas")
    if MMPE in modules:
        path = '../../MMPE/mmpe'
        for root, folders, files in os.walk(path):
            if (root != path and
                '.git' not in root and
                'test' not in root.lower() and
                'build_exe' not in root and
                'cython_compile' not in root and
                'module_template' not in root and
                'MyQt' not in root and
                'QtGuiLoader' not in root and
                'mmpe\\ui' not in root):
                for file in [f for f in files if os.path.splitext(f)[1] == ".py" and
                                                        'test' not in f.lower()]:
                    module = os.path.splitext(os.path.join(os.path.relpath(root, path), file))[0].replace(os.path.sep, '.')
                    includes.append("mmpe.%s" % module)
    if PARAMIKO in modules:
        includes.append("cryptography.hazmat.backends.openssl.backend")
        includes.append("cryptography.fernet")
        includes.append("_cffi_backend")
        includes.append("_ssl")

    for m in modules:
        try:
            excludes.remove(m)
        except ValueError:
            pass

    for i in includes:
        try:
            excludes.remove(i)
        except ValueError:
            pass


    imports = "\n".join(imports)
    if include_files:
        strings = "'" + "','".join([v for v in include_files if not str(v)[0] == "("]) + "'"
        tuples = ",".join([str(v) for v in include_files if str(v)[0] == "(" and str(v)[-1] == ")"])
        include_files = "[" + ",".join((strings, tuples)) + "]"
        #include_files = include_files.replace("""'(matplotlib.get_data_path(),"mpl-data")'""", """(matplotlib.get_data_path(), "mpl-data")""")
    if includes:
        includes = "['" + "','".join(includes) + "']"

    if icon is not None:
        icon = "icon='%s', " % icon
    else:
        icon = ""
    executables = ["""Executable("%s.py", %s%sshortcutName="%s", shortcutDir="DesktopFolder")""" % (name, base, icon, name)]
    for ae in additional_executables:
        if isinstance(ae, tuple):
            ae, b = ae
        else:
            b = base
        executables.append("""Executable("%s", %s)""" % (ae, b))
    executables = ",".join(executables)

    with open('setup.py', 'w') as fid:
        fid.writelines("""from cx_Freeze import setup, Executable
%s
try:
    import set_path
    set_path.set_path()
except:
    pass
import os
os.environ['TCL_LIBRARY'] = r"C:\\Anaconda3\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = r"C:\\Anaconda3\\tcl\\tk8.6"

build_exe_options = {
"include_msvcr": True,
"includes": %s,
"packages": %s,
'excludes' : %s,
"include_files": %s,
"zip_includes": %s}

setup(
name = "%s",
version="%s",
description="%s",
author = "%s",
options = { "build_exe": build_exe_options},
executables = [%s])
    """ % (imports, includes, packages, excludes, include_files, zip_includes, name, version, description, author, executables))
    print ("setup.py writing finished")


def prepare(modules):
    clean(modules)
    if GUIDATA in modules:
        if not os.path.isdir("guidata"):
            os.mkdir("guidata/")
        if not os.path.isdir("guidata/images/"):
            import site
            for f in site.getsitepackages():
                if "guidata" in os.listdir(f):
                    shutil.copytree(r"%s/guidata/images/" % f, "guidata/images/")
            #shutil.copytree(r"%s/Lib/site-packages/guidata/images/" % os.path.dirname(sys.executable), "guidata/images/")
    if PYQT4 in modules or PYQT4LIM in modules:
        copy_imageformats()
    if DOCX in modules:
        from mmpe.docx_document import docx_document
        source_path = os.path.dirname(docx_document.__file__)
        dest_path = "mmpe/docx_document/"
        make_dirs(dest_path)
        for folder in ['docx-template_clean'][:1]:
            if folder not in os.listdir(dest_path):
                shutil.copytree(os.path.join(source_path, folder), os.path.join(dest_path, folder))



def clean(modules):
    if modules and GUIDATA in modules:
        if os.path.isdir("guidata"):
            shutil.rmtree("guidata/")
    if modules and PYQT4 in modules:
        if os.path.isdir('imageformats'):
            shutil.rmtree('imageformats/')
    if modules and DOCX in modules:
        if 0 and os.path.isdir('mmpe'):
            shutil.rmtree('mmpe')
    if modules and SCIPY in modules:
        try:
            from scipy.sparse.sparsetools import csr, csc, coo, dia, bsr, csgraph
            for f in [csr._csr.__file__,
                      csc._csc.__file__,
                      coo._coo.__file__,
                      dia._dia.__file__,
                      bsr._bsr.__file__,
                      csgraph._csgraph.__file__]:
                if os.path.isfile(os.path.basename(f)):
                    os.remove(os.path.basename(f))
        except ImportError:
            pass
    if modules and HDF5 in modules:
        import platform
        if platform.architecture()[0] == "32bit":
            from h5py import _conv, _errors, _objects, _proxy, defs, h5, h5a, h5d, h5ds, h5f, h5fd, h5g, h5i, h5l, h5o, h5p, h5r, h5s, h5t, h5z, utils
            for f in [_conv, _errors, _objects, _proxy, defs, h5, h5a, h5d, h5ds, h5f, h5fd, h5g, h5i, h5l, h5o, h5p, h5r, h5s, h5t, h5z, utils]:
                filename = "h5py.%s" % os.path.basename(f.__file__)
                if os.path.isfile(filename):
                    os.remove(filename)

        shutil.rmtree("h5py/", ignore_errors=True)



def copy_imageformats():
    """
    Run this function if icons are not loaded
    """
    from PyQt4 import QtCore
    import sys
    app = QCoreApplication(sys.argv)
    qt_library_path = QCoreApplication.libraryPaths()


    imageformats_path = None
    for path in qt_library_path:
        if os.path.exists(os.path.join(str(path), 'imageformats')):
            imageformats_path = os.path.join(str(path), 'imageformats')
            local_imageformats_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'imageformats')
            local_imageformats_path = os.path.join(os.getcwd(), 'imageformats')
            if not os.path.exists(local_imageformats_path):
                os.mkdir(local_imageformats_path)
            for file in glob.glob(os.path.join(imageformats_path, '*')):
                shutil.copy(file, os.path.join(local_imageformats_path, os.path.basename(file)))

