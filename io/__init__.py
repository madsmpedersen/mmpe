import os
d = None;d = dir()


from .make_dirs import make_dirs, make_packages

def read_file(path, default=None):
    if os.path.isfile(path):
        with open(path) as fid:
            return fid.read()
    else:
        return default

__all__ = [m for m in set(dir()) - set(d)]