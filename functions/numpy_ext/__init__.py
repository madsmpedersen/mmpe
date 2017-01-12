
d = None
d = dir()

from mmpe.functions.numpy_ext import fourier_fit


import numpy as np


def nanstd(x):
    return [lambda x : np.nanstd(x), lambda x: np.nan][len(x) == 0](x)
def nanvar(x):
    return [lambda x : np.nanvar(x), lambda x: np.nan][len(x) == 0](x)
def nanmean(x):
    return [lambda x : np.nanmean(x), lambda x: np.nan][len(x) == 0](x)


def bin(x, y=None, bins=10, npfunc=nanmean, return_empty_bins=True):
    """Bin and mean data

    Parameters
    ----------
    x : array_like
        x array to bin over
    y : array_like, optional
        y array with 'weights'
    bins : array_like or int, optional
        if array_like: Bin edges
        if int: Number of bins, default is 10
    npfunc : numpy function
        Numpy function to map to y observations in each bin.\n
        Normally np.mean(default) or np.median
    return_empty_bins : boolean, optional
        if True, default, NAN is return for empty bins
        if False, empty bins are not returned

    Returns
    -------
    bin_x : array
        Values of each bin (i.e. mean of x for each bin)
    bin_y : array
        npfunc(default is mean) mapped to y observations in each bin
    bin_count : array
        Number of observations in each bin
    bin_edges : array
        Bin edges

    Examples
    --------
    >>> bin_x, bin_y, bin_count, bin_edges = bin(numpy.random.random(100))

    """

    if y is None:
        y = x
    x, y = np.array(x[:]), np.array(y[:])
    assert len(x) == len(y), "x and y must have same length (%d!=%d)" % (len(x), len(y))

    if isinstance(bins, int):
        bins = np.linspace(np.nanmin(x), np.nanmax(x) + 1e-10, bins + 1)
    digitized = np.digitize(x, bins)
    #digitized[digitized == len(bins)] = len(bins) - 1
    digitized[np.isnan(x) | np.isnan(y)] = -1

    def func(x):
        if len(x):
            return npfunc(x)
        return np.nan
    res = (np.array([nanmean(x[digitized == i]) for i in range(1, len(bins))]),
            np.array([func(y[digitized == i]) for i in range(1, len(bins))]),
            np.array([np.sum(digitized == i) for i in range(1, len(bins))]),
            bins)
    if return_empty_bins:
        return res
    else:
        bin_count = res[2]
        return [v[bin_count > 0] for v in res]

def bin2(x, y=None, bins=10, npfunc=nanmean, return_empty_bins=True):
    """Bin and mean data

    Parameters
    ----------
    x : array_like
        x array to bin over
    y : array_like, optional
        y array with 'weights'
    bins : array_like or int, optional
        if array_like: Bin edges
        if int: Number of bins, default is 10
    npfunc : numpy function
        Numpy function to map to y observations in each bin.\n
        Normally np.mean(default) or np.median
    return_empty_bins : boolean, optional
        if True, default, NAN is return for empty bins
        if False, empty bins are not returned

    Returns
    -------
    bin_x : array
        Values of each bin (i.e. mean of x for each bin)
    bin_y : array
        npfunc(default is mean) mapped to y observations in each bin
    bin_count : array
        Number of observations in each bin
    bin_edges : array
        Bin edges
    bin_mean_edge : array
        mean of the edges of each bin
    std_bin_x : array
        standard deviation of x values in each bin
    std_bin_y : array
        standard deviation of y values in each bin

    Examples
    --------
    >>> bin_x, bin_y, bin_count, bin_edges, bin_mean_edge, std_bin_x, std_bin_y = bin2(numpy.random.random(100))

    """

    if y is None:
        y = x
    x, y = np.array(x[:]), np.array(y[:])
    assert len(x) == len(y), "x and y must have same length (%d!=%d)" % (len(x), len(y))

    if isinstance(bins, int):
        bins = np.linspace(np.nanmin(x), np.nanmax(x) + 1e-10, bins + 1)
    else:
        bins=np.array(bins)
    digitized = np.digitize(x, bins)
    #digitized[digitized == len(bins)] = len(bins) - 1
    digitized[np.isnan(x) | np.isnan(y)] = -1

    def func(x):
        if len(x):
            return npfunc(x)
        return np.nan
    with np.errstate(all='ignore'):
        res = (np.array([nanmean(x[digitized == i]) for i in range(1, len(bins))]),
                np.array([func(y[digitized == i]) for i in range(1, len(bins))]),
                np.array([np.sum(digitized == i) for i in range(1, len(bins))]),
                bins,
                (bins[1:] + bins[:-1]) / 2,
                np.array([nanstd(x[digitized == i]) for i in range(1, len(bins))]),
                np.array([nanstd(y[digitized == i]) for i in range(1, len(bins))])
                )
    if return_empty_bins:
        return res
    else:
        bin_count = res[2]
        return [v[bin_count > 0] for v in res]


#
#digitized = numpy.digitize(data, bins)
#
#bin_means = [data[digitized == i].mean() for i in range(1, len(bins))]

__all__ = [m for m in set(dir()) - set(d)]



if __name__ == "__main__":
    import matplotlib.pyplot as plt
    bin_count, bin_y_mean, bin_x, bin_edges = bin([10, 3, 5, 6, 73, 1, 34, 5, 3, 2, 3, 4, 26], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    print (bin_count, bin_y_mean, bin_x, bin_edges)
    plt.plot(bin_x, bin_y_mean, '.')
    plt.show()
