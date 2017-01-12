from mmpe.cython_compile.cython_compile import cython_compile


@cython_compile
def score_dict_cython(n):
    return n * 2
