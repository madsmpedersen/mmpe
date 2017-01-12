'''
Created on 11/04/2014

@author: MMPE
'''

import numpy as np
import matplotlib
from matplotlib.textpath import TextPath
import matplotlib.axis as maxis
from matplotlib.ticker import MaxNLocator
class AutoLocator(MaxNLocator):
    """Tick locator that tries to be smart.

    Parameters
    ----------
    nbins : int
        Maximum number of bins---i.e., tick intervals.

    steps : list of numbers
        Allowable steps for lowest displayed digit. This is a sequence of
        "nice" numbers starting with 1 and ending with 10.

    """
    def __init__(self, nbins=9, steps=[1, 2, 5, 10]):
        MaxNLocator.__init__(self, nbins=nbins, steps=steps)
        self._nbins_cached = nbins

    def bin_boundaries(self, vmin, vmax):
        """Return bin boundaries (a.k.a. tick locations)."""

        # The calculation of the label width should actually depend on the
        # tick Formatter instance.
        label_width = max(len('%g' % v) for v in (vmin, vmax))

        label_px_width = 1.2 * TextPath((0, 0), '0' * (label_width + 2)).get_extents().width
        w, _ = self.axis.axes.figure.canvas.get_width_height()

        if not isinstance(self.axis, maxis.XAxis):
            raise NotImplementedError("Currently only XAxis is supported.")
        # Use figure width to calculate the number of bins---only valid for x-axis.
        # The following nbins calculation is approximate since it should vary
        # with subplot parameters---i.e. padding on the left and right of
        # subplots and multiple columns in a subplot grid.
        self._nbins = min(self._nbins_cached, int(w / label_px_width))
        return MaxNLocator.bin_boundaries(self, vmin, vmax)

