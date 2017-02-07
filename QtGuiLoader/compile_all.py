'''
Created on 18/06/2012

@author: Mads
'''
import os
import sys

from mmpe.QtGuiLoader.QtGuiLoader import pyqt_compile_func
import qtpy

ui_compiler = pyqt_compile_func
def _compile_all(path, compile_func):

    def get_ui_list(path):
        ui_list = []
        if os.path.isdir(path):
            #search files and sub-packages
            for f in os.listdir(path):
                if f not in ['dist']:
                    ui_list += get_ui_list(os.path.join(path, f))
        else:
            #search file
            if path.endswith(".ui"):
                ui_list.append(path)
        return ui_list

    exe_dir = os.path.dirname(sys.executable)
    os.environ['PATH'] = "%s;%s;%s/scripts" % (os.environ['PATH'], exe_dir, exe_dir)
    os.environ['WINPYDIR'] = exe_dir
    api = qtpy.QtCore.Qt.__module__.replace(".QtCore","")
    for ui_file in get_ui_list(path):
        py_file = ui_file.replace(".ui", ".py")


        if os.path.exists(py_file):
            with open(py_file) as fid:
                recompile = api not in fid.read()

        if not os.path.exists(py_file) or \
            os.path.getmtime(ui_file) > os.path.getmtime(py_file) or \
            os.path.getsize(py_file) == 0 or \
            recompile:
            print ("compile %s > %s" % (ui_file, py_file))
            compile_func(ui_file, py_file)

            #os.system("%s %s > %s" % (compiler, ui_file, py_file))

        else:
            #print "%s: ok" % py_file
            pass
    print ("Finish compiling UI")


def compile_all(path="."):
    print ("ui_compiler" + ui_compiler)
    _compile_all(path, ui_compiler)

def compile_all_pyqt(path="."):
    _compile_all(path, pyqt_compile_func)

# def compile_all_pyside(path="."):
#     os.environ['QT_API'] = "pyside"
# 
#     _compile_all(path, pyside_compile_func)

if "__main__" == __name__:
    import os
    path = r"C:\mmpe\python\pydap_redmine\trunk"
    print (os.path.realpath(path))
    compile_all_pyqt(path)
