import sys
from mmpe.ui import OutputUI, UI, StatusUI

class DaemonOutputUI(OutputUI, StatusUI):
    def __init__(self, parent=None):
        OutputUI.__init__(self, parent=parent)
        StatusUI.__init__(self, parent=parent)
        
    
    def show_error(self, msg, title="Error"):
        if isinstance(msg, Exception):
            title = msg.__class__.__name__
            msg = str(msg)
        sys.stderr.write("%s\n%s" % (title, msg))


class DaemonUI(DaemonOutputUI, UI):
    pass
