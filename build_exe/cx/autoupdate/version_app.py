import sys
import esky
from mmpe.build_exe.cx.autoupdate.myesky import MyEsky
import os
from esky import Esky
from mmpe.build_exe.cx.autoupdate import myesky
version = (1, 1, 35)
if __name__ == "__main__":
    print (str(version))
    print (hasattr(sys, "frozen"))
    if 1 or hasattr(sys, "frozen"):

        app = Esky(sys.executable, r"http://tools.windenergy.dtu.dk/pdap/downloads/versions.txt")
        app.auto_update(myesky.callback)
