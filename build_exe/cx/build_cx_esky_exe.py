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
import matplotlib
NUMPY = 'numpy'
MATPLOTLIB = 'matplotlib'
GUIDATA = 'guidata'
PYQT4 = 'PyQt4'
PYSIDE = 'PySide'
SCIPY = 'scipy'
CTYPES = '_ctypes'
MULTIPROCESSING = '_multiprocessing'
DOCX = "docx"
OPENGL = "_opengl"
PIL = "PIL"
HDF5 = "h5py"
PANDAS = 'pandas'
ESKY = "ESKY"



def build_esky_exe(filename, version="1.0.0", description="", author="", modules=[NUMPY], includes=[], include_files=[], icon=None, gui_only="True"):
    modules.append(ESKY)
    basename = filename.replace('.py', '')
    folder = '%s_dist/' % basename
    prepare(modules)
    write_setup(basename, version, description, author, modules, includes, include_files, icon, gui_only)

    if os.path.isdir(folder):
        shutil.rmtree(folder)
    #exec(compile(open('setup.py').read(), 'setup.py', 'exec'))
    os.system('%s setup.py' % sys.executable)
    #shutil.move('./build/', folder)
    #os.remove('setup.py')
    clean(modules)

    print ("distribution created (%s/)" % folder)



def write_setup(name, version, description="", author="", modules=[NUMPY], includes=[], include_files=[], icon=None, gui_only="True"):
    """['appfuncs','gui_test']"""
    """["graphics/", "imageformats/", ]"""
    """"includes":["sip"],"""
    imports = []
    base = ""
    excludes = ['PyQt4.uic.port_v3', 'Tkconstants', 'tcl', 'tk', 'doctest', '_gtkagg', '_tkagg', 'bsddb',
                'curses', 'pywin.debugger', 'pywin.debugger.dbgcon', 'pywin.dialogs', 'Tkinter',
                'tables', 'zmq', 'win32', 'Pythonwin', 'Cython', 'statmodels', 'cvxopt', '_sqlite3', '_ssl', '_testcapi',
                'markupsafe', 'numexpr', '_elementtree', '_hashlib', '_testcapi', 'simplejson', 'pyexpat', "lxml",
                MATPLOTLIB, GUIDATA, PYQT4, PYSIDE, SCIPY, NUMPY, MULTIPROCESSING, DOCX, OPENGL, PIL, HDF5]
    def add(module):
        try:
            excludes.remove(module)
        except:
            pass
    #'pandas', '_socket', 'sip',
    if MATPLOTLIB in modules:
        mpl_path = matplotlib.get_data_path()
        include_files.append(('mpl-data', mpl_path))
        imports.append("import matplotlib")


    if GUIDATA in modules:
        include_files.append("guidata/images/")
    if PYQT4 in modules:
        #include_files.append("imageformats/")
        includes.append("sip")
        includes.append("PyQt4.QtWebKit")
        includes.append("PyQt4.QtNetwork")
        includes.append("PyQt4.Qsci")
#        includes.append("PyQt4.uic")
#        includes.append("PyQt4.uic.port_v3")

        base = "base='Win32GUI', "
    if SCIPY in modules:
        imports.append("import scipy.sparse.csgraph")
        includes.extend(["scipy.sparse.csgraph._validation", "scipy.sparse.linalg.dsolve.umfpack",
        "scipy.integrate.vode", "scipy.integrate._ode", "scipy.integrate.lsoda"])
        includes.append("scipy.special._ufuncs_cxx")  #py3_64
        from scipy.sparse.sparsetools import csr, csc, coo, dia, bsr, csgraph

        for f in [csr._csr.__file__,
                  csc._csc.__file__,
                  coo._coo.__file__,
                  dia._dia.__file__,
                  bsr._bsr.__file__,
                  csgraph._csgraph.__file__]:
            shutil.copy(f, os.path.basename(f))
            include_files.append("%s" % os.path.basename(f))

    if DOCX in modules:
        include_files.append("functions/docx_document/docx-template_clean/")
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
        includes.append("h5py")
        includes.append('h5py.h5ac')


    if PANDAS in modules:
        #add('email')
        includes.append("Pandas")

    for m in modules:
        try:
            excludes.remove(m)
        except ValueError:
            pass


    imports = "\n".join(imports)
    if include_files:
        #while any([os.path.isdir(f) for f in include_files if isinstance(f, str)]):
        #    for folder in [f for f in include_files if isinstance(f, str) and os.path.isdir(f)]:
        #        include_files.remove(folder)
        #        include_files.extend(os.listdir(folder))
        include_files = "[" + ",".join([("'%s'" % str(f), str(f))[isinstance(f, tuple)] for f in include_files]) + "]"
        include_files = include_files.replace("""'(matplotlib.get_data_path(),"mpl-data")'""", """(matplotlib.get_data_path(), "mpl-data")""")
    if includes:
        includes = "['" + "','".join(includes) + "']"

    if icon is not None:
        icon = "icon='%s', " % icon
    else:
        icon = ""

    with open('setup.py', 'w') as fid:
        fid.writelines("""from distutils.core import setup
from esky import bdist_esky
from esky.bdist_esky import Executable
%s

build_exe_options = {
"includes": %s,
'excludes' : %s,
'freezer_module': "cxfreeze",

}
executable = Executable("%s.py", %s gui_only=%s)
setup(
name = "%s",
version="%s",
description="%s",
author = "%s",
scripts = [executable],
data_files = %s,
script_args = ("bdist_esky",),
options = { "bdist_esky": build_exe_options})
    """ % (imports, includes, excludes, name, icon, gui_only, name, version, description, author, include_files))


def prepare(modules):
    clean(modules)
    if GUIDATA in modules:
        if not os.path.isdir("guidata"):
            os.mkdir("guidata/")
        if not os.path.isdir("guidata/images/"):
            shutil.copytree(r"%s/Lib/site-packages/guidata/images/" % os.path.dirname(sys.executable), "guidata/images/")
    if PYQT4 in modules:
        copy_imageformats()
    if DOCX in modules:
        from mmpe.docx_document import docx_document
        source_path = os.path.dirname(docx_document.__file__)
        dest_path = "functions/docx_document/"
        make_dirs(dest_path)
        for folder in ['docx-template_clean', 'inkscape']:
            shutil.copytree(os.path.join(source_path, folder), os.path.join(dest_path, folder))



def clean(modules):
    if modules and GUIDATA in modules:
        if os.path.isdir("guidata"):
            shutil.rmtree("guidata/")
    if modules and PYQT4 in modules:
        if os.path.isdir('imageformats'):
            shutil.rmtree('imageformats/')
    if modules and DOCX in modules:
        if os.path.isdir('functions'):
            shutil.rmtree('functions')
    if modules and SCIPY in modules:
        from scipy.sparse.sparsetools import csr, csc, coo, dia, bsr, csgraph
        for f in [csr._csr.__file__,
                  csc._csc.__file__,
                  coo._coo.__file__,
                  dia._dia.__file__,
                  bsr._bsr.__file__,
                  csgraph._csgraph.__file__]:
            if os.path.isfile(os.path.basename(f)):
                os.remove(os.path.basename(f))
    if modules and HDF5 in modules:
        #from h5py import _conv, _errors, _objects, _proxy, defs, h5, h5a, h5d, h5ds, h5f, h5fd, h5g, h5i, h5l, h5o, h5p, h5r, h5s, h5t, h5z, utils
        #for f in [_conv, _errors, _objects, _proxy, defs, h5, h5a, h5d, h5ds, h5f, h5fd, h5g, h5i, h5l, h5o, h5p, h5r, h5s, h5t, h5z, utils]:
        #    f = f.__file__
        #    shutil.copy(f, "h5py." + os.path.basename(f))
        #    include_files.append("'h5py.%s'" % os.path.basename(f))
        shutil.rmtree("h5py/", ignore_errors=True)



def copy_imageformats():
    """
    Run this function if icons are not loaded
    """
    from PyQt4 import QtCore
    import sys
    app = QtCore.QCoreApplication(sys.argv)
    qt_library_path = QtCore.QCoreApplication.libraryPaths()


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

