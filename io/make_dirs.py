'''
Created on 06/02/2014

@author: MMPE
'''
import os
import errno

def make_dirs(path):
    path = os.path.realpath(os.path.dirname(path))
    folders = path.split(os.path.sep)

    for i in range(len(folders)):
        folder = os.path.sep.join(folders[:i + 1])
        if folder != "":
            if os.path.ismount(folder):
                continue
            try:
                os.mkdir(folder)
            except OSError as exception:
                if exception.errno != errno.EEXIST:
                    raise

def make_packages(path):
    path = os.path.realpath(os.path.dirname(path))
    folders = path.split(os.path.sep)

    for i in range(len(folders)):
        folder = os.path.sep.join(folders[:i + 1])
        try:
            os.mkdir(folder)
            init_path = os.path.join(folder, "__init__.py")
            if not os.path.isfile(init_path):
                with open(init_path, 'w') as fid:
                    pass
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
