'''
Created on 20/05/2014

@author: MMPE
'''
import numpy as np

def minimize(func, bounds, args=(), kwargs={}, max_iter=10, tolerance=0.01, overlap=.1, verbose=False):
    def p(s, v=None):
        if verbose:
            if v is None:
                print(s)
            elif isinstance(v, int):
                print ("%s: %d" % (s, v))
            else:
                if v.shape[0] == 1:
                    print ("%s: %s" % (s, v[0]))
                else:
                    print ("%s:\n%s" % (s, v))

    bounds = np.atleast_2d(np.array(bounds)).astype(np.float)
    if bounds.shape[0] == 2 and bounds.shape[1] != 2:
        bounds = bounds.T
    errors = np.atleast_2d(np.array([func(bounds[:, 0], *args, **kwargs), func(bounds[:, 1], *args, **kwargs)]).T)
    exchange_indexes = errors[:, 0] > errors[:, 1]
    bounds[exchange_indexes] = bounds[exchange_indexes][::-1]
    errors[exchange_indexes] = errors[exchange_indexes][::-1]

    p('-' * 50)
    p("Initial bounds:", bounds)
    p("Initial errors:", errors)

    for i in range(max_iter):
        f = np.zeros_like(errors[:, 0])
        mask = errors[:, 0] != errors[:, 1]
        f[mask] = -errors[mask, 0] / (errors[mask, 1] - errors[mask, 0])
        f += overlap * f * ((np.abs(errors[:, 1]) > abs(errors[:, 0])).astype(np.int) * 2 - 1)  # reward farther bound, to move that first
        bounds[f == 0, 0] = bounds[f == 0, 1]
        values = bounds[:, 0] + (bounds[:, 1] - bounds[:, 0]) * f

        error = func(values, *args, **kwargs)
        replace_index = (abs(errors[:, 1]) > abs(errors[:, 0])).astype(np.int)
        bounds[np.arange(bounds.shape[0]), replace_index] = values
        errors[np.arange(bounds.shape[0]), replace_index] = error
        if np.max(abs(bounds[:, 1] - bounds[:, 0])) < tolerance:
            break
        p("Iteration:", (i + 1))
        p("Value:", values)
        p("New bounds:", bounds)
        p("New errors:", errors)

    p("Iterations:", (i + 1))
    p("Final value:", values)
    p("Final bounds:", bounds)
    p("Final errors:", errors)
    p("")

    return values, i, bounds, errors


if __name__ == "__main__":
    def t(a):
        return 5 - a + .1 * (5 - a)
    bounds = np.array([3, 6])
    print (minimize(t, bounds, verbose=False))
    print ("")
    def t(args):
        a, b = args
        return [-(5 - a + .1 * (5 - a)), -(9 - b + .1 * (9 - b))]
    bounds = np.array([[3, 6], [12, 7]])
    print (minimize(t, bounds, verbose=False))
