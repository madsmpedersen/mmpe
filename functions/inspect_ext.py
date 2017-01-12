'''
Created on 10/04/2014

@author: MMPE
'''


import inspect
import os
import time
import zipfile
import types
import sys
import traceback




def class_list(func_path, base_class, exclude_classes=[]):
    exclude_classes.append(base_class)
    class_lst = []

    dirname = os.path.dirname(os.path.relpath(func_path))
    if not sys.path[0] == dirname:
        sys.path.insert(0, dirname)


    file_lst = []
    for root, _, files in os.walk(func_path):
        file_lst.extend([os.path.relpath(os.path.join(root, f), dirname) for f in files if f.lower().endswith('.py')])

    if zipfile.is_zipfile('library.zip'):
        z = zipfile.ZipFile('library.zip')
        file_lst.extend([os.path.relpath(f) for f in z.namelist() if f.startswith(func_path)])

    for module_name in [os.path.splitext(f)[0].replace(os.path.sep, ".") for f in file_lst]:

        t = time.time()
        try:
            module = __import__(module_name, {}, {}, ['*'])
            class_lst.extend([cls for cls in module.__dict__.values()
                              if inspect.isclass(cls) and issubclass(cls, base_class) and not cls in exclude_classes])
        except Exception as e:
            class_lst.append(type(e)("Failed to import %s\n" % module_name + str(e)).with_traceback(sys.exc_info()[2]))
            #tb = "".join(traceback.format_tb(sys.exc_info()[2])).replace(r"""File ".\%s""" % func_path, r"""File "%s""" % os.path.realpath(func_path))
            #class_lst.append(type(e)("Failed to import %s\n" % (tb, module_name) + str(e)))
        if time.time() - t > 1:
            print (module_name, time.time() - t)
    return class_lst


def argument_string(func):
    if hasattr(func, 'target_function'):
        func = func.target_function
    try:
        args, varargs, keywords, defaults = inspect.getfullargspec(func)[:4]
        if defaults is not None:
            for nr in range(1, len(defaults) + 1):
                d = defaults[-nr]
                if isinstance(d, str):
                    d = "'%s'" % d
                elif isinstance(d, types.FunctionType) and hasattr(d, "__name__"):
                    if d.__module__.startswith('numpy.'):
                        d = "np.%s" % d.__name__
                    else:
                        d = d.__name__
                elif isinstance(d, type):
                    d = str(d).split("'")[1].replace("numpy", "np")
                args[-nr] = "%s=%s" % (args[-nr], d)

        if varargs is not None:
            args.append("*%s" % varargs)

        if keywords is not None:
            args.append("**%s" % keywords)

        if len(args) > 0 and args[0] == 'self':
            return "(%s)" % ", ".join(args[1:])  # remove self
        else:
            return "(%s)" % ", ".join(args)
    except TypeError:
        return ""
