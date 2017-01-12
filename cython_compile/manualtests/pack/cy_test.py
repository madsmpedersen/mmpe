from wetb.utils.cython_compile.cython_compile import cython_compile


@cython_compile
def CyTest(n):
    return __file__.endswith(".pyd"), n * 2