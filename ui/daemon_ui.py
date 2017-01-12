import sys
from mmpe.ui import OutputUI, UI

class DaemonOutputUI(OutputUI):
    def show_error(self, msg, title="Error"):
        if isinstance(msg, Exception):
            title = msg.__class__.__name__
            msg = str(msg)
        sys.stderr.write("%s\n%s" % (title, msg))


class DaemonUI(DaemonOutputUI, UI):
    pass
