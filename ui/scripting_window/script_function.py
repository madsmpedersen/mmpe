from qtpy import QtGui
import inspect
import os
import zipfile
from mmpe.functions.timing import print_time
import time
class ScriptFunction(object):
    class_name = None
    def __init__(self, controller, gui, model, name):
        self.controller = controller
        self.gui = gui
        self.model = model
        self.name = name
        self.__name__ = name
        self.class_name = self.__class__.__name__


@print_time
def script_function_class_list(func_path, exclude_classes=[]):
    exclude_classes.append(ScriptFunction)
    class_lst = []

    file_lst = []
    for root, _, files in os.walk(func_path):
        file_lst.extend([os.path.join(root, f) for f in files if f.lower().endswith('.py')])

    if zipfile.is_zipfile('library.zip'):
        z = zipfile.ZipFile('library.zip')
        file_lst.extend([f for f in z.namelist() if f.startswith(func_path)])


    for module_name in [os.path.splitext(f)[0].replace("\\", ".").replace("/", ".") for f in file_lst]:
        t = time.time()
        module = __import__(module_name, {}, {}, ['*'])
        class_lst.extend([cls for cls in module.__dict__.values()
                          if inspect.isclass(cls) and  issubclass(cls, ScriptFunction) and not cls in exclude_classes])
        if time.time() - t > 0.1:
            print (module_name, time.time() - t)
    return class_lst


