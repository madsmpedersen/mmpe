'''
Created on 10/07/2014

@author: MMPE
'''



def deep_encode(obj, *args):
    if isinstance(obj, bytes):
        return obj
    if isinstance(obj, (list, tuple)):
        return [deep_encode(o) for o in obj]
    return obj.encode(*args)

def to_str(obj, *args):
    return deep_decode(obj, *args)


def deep_decode(obj, *args):
    if isinstance(obj, str):
        return obj
    elif isinstance(obj, bytes):
        return obj.decode(*args)
    elif isinstance(obj, (list, tuple)):
        return [deep_decode(o, *args) for o in obj]
    else:
        raise NotImplementedError(obj, obj.__class)



def to_bytes(obj, *args):
    return deep_encode(obj, *args)
