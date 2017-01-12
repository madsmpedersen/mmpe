import inspect
from functools import wraps
def print_class_name(fn):
    """
    A decorator that prints the name of the class of a bound function (IE, a method).
    This version works with Python 2.6.

    NOTE: This MUST be the first decorator applied to the function! E.g.:

        @another_decorator
        @yet_another_decorator
        @print_class_name
        def my_fn(stuff):
            pass

    This is because decorators replace the wrapped function's signature.
    """
    @wraps(fn)
    def inner(*args, **kwargs):
        arg_spec = inspect.getargspec(fn)

        # We assume that if a parameter named `self` exists for the wrapped
        # function, the function is bound to a class, and we can get the name of
        # the class from the function's first argument.
        if 'self' in arg_spec.args:
            cls = args[0].__class__
            print ('Function bound to class %s' % cls.__name__)
        else:
            print ('Unbound function!')

        return fn(*args, **kwargs)
    return inner

class testA(object):
    @print_class_name
    def A(self):
        return 1

testA.A()
