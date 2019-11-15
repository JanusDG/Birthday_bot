import statistics


def standard_deviation(lst):
    """
    list -> float

    Return the standard deviation of variables in list.

    >>> standard_deviation([25.8, 0.4, 10.2, 3.7, 2.9, 5.7])
    9.26
    """
    return round(statistics.stdev(lst), 2)


def mode(lst):
    """
    list -> float

    Return the mode of variables in list.

    >>> mode([7, 1.3, 1.3, 1.2, 49, 7, 80, 3, 7])
    7
    """
    nd = []
    for i in lst:
        el = lst.count([i])
        nd.append(el)
    index = nd.index(max(nd))
    return lst[index]


def median(lst):
    """
    list -> float

    Return the median of variables in list.

    >>> median([1, 3, 5, 15, 4, 7])
    4.5
    """
    if len(lst) % 2 != 0:
        median = sorted(lst)[int(len(lst) / 2)]
    else:
        median = (sorted(lst)[int(len(lst) / 2)] +
                  sorted(lst)[int((len(lst) / 2)) - 1]) / 2
    return median

def mean(lst):
    """
    list -> float

    Return the average meaning of variables in list.

    >>> mean([200, 300, 600, 800, 700])
    520.0
    """
    return round(sum(lst)/len(lst), 2)


def harmonic_mean(lst):
    """
    list -> float

    Return the harmonic meaning of variables in list.

    >>> harmonic_mean([20, 15.5, 10])
    13.98
    """
    return round(statistics.harmonic_mean(lst), 2)


def geometric_mean(lst):
    """
    list -> float

    Return the averege geometric meaning of variables in list.

    >>> geometric_mean([22, 10])
    15.0
    """
    prod = 1
    for i in lst:
        prod *= i
    return round(prod ** (1/len(lst)), 2)
