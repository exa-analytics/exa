# -*- coding: utf-8 -*-
'''
JiT Compiled Functions
===========================================

'''
from numba import njit, vectorize, typeof
from numba import int64, float64, int32, float32
from exa import np


# Custom types
i8i8 = typeof((1, 1))


# Functions related to index generation (indexes are always int64)
@njit(cache=True)
def gen_idxs_lbins_counts(lbins, counts):
    '''
    Generates indices using left bins as starting points.

    Generates two unique (identical length) indices as well as the selection
    range from a set of (left) bin edges and counts. Return type of each array
    is 64-bit integer (default index type).

    Example:
        >>> import numpy as np
        >>> lbins = np.array([0, 5, 100])
        >>> counts = np.array([1, 3, 2])
        >>> f1, f2, f3 = gen_idxs_lbins_counts(lbins, counts)
        >>> print(f1)
        [0 1 1 1 2 2]
        >>> print(f2)
        [0 0 1 2 0 1]
        >>> print(f3)
        [  0   5   6   7 100 101]

    Args:
        lbins (:class:`~numpy.ndarray`): Starting indices
        counts (:class:`~numpy.ndarray`): Length from each starting index

    Returns:
        tup (tuple): Tuple of 3 equal length arrays (bins, ranges, indices)
    '''
    n = np.sum(counts)    # Total size
    first = np.empty((n, ), dtype=int64)
    second = np.empty((n, ), dtype=int64)
    indices = np.empty((n, ), dtype=int64)
    k = 0
    for i, start in enumerate(lbins):
        for j, index in enumerate(range(start, start + counts[i])):
            first[k] = i
            second[k] = j
            indices[k] = index
            k += 1
    return first, second, indices


@njit(cache=True)
def get_idxs_by_values(values, positions):
    '''
    Get indexes by values from a positions array.

    Examples:
        >>> import numpy as np
        >>> t1 = np.array([1, 2, 3, 4], dtype='i8')
        >>> t2 = np.array([3, 2, 1, 10, 4], dtype='i8')
        >>> get_idxs_by_values(t1, t2)
        array([2, 1, 0, 4], dtype=int64)
    '''
    indexes = np.empty((len(values), ), dtype=int64)
    for i, value in enumerate(values):
        val = np.where(positions == value)[0]
        indexes[i] = np.NaN if len(val) == 0 else val[0]
    return indexes


# Mapping/pairing functions
@njit([int64(int64, int64), int64(int64, int32),
       int64(int32, int64), int64(int32, int32)], cache=True)
def szudzik_pair(int1, int2):
    '''
    Compute the `Szudzik`_ number for a pair of integers.

    Generates a unique integer from two integers using the pairing
    algorithm of `Szudzik`_. This is a type of primitive
    recursive bijective `pairing function`_.

    Example:
        >>> szudzik_pair(1, 1)
        3
        >>> szudzik_pair(2, 3)
        11

    Args:
        int1 (int): First integer
        int2 (int): Second integer

    Returns:
        szudzik_number (int): Unique integer

    See Also:
        :func:`~exa.jitted.szudzik_unpairing`

    .. _Szudzik: http://szudzik.com/ElegantPairing.pdf
    .. _pairing function: https://en.wikipedia.org/wiki/Pairing_function
    '''
    if int1 == max(int1, int2):
        return int1**2 + int1 + int2
    else:
        return int2**2 + int1


@njit([i8i8(int64), i8i8(int32)], cache=True)
def szudzik_unpair(szudzik_number):
    '''
    Generates the original integers used to create `Szudzik`_
    number.

    Example:
        >>> szudzik_unpair(3)
        (1, 1)
        >>> szudzik_unpair(11)
        (2, 3)

    Args:
        szudzik_number (int): The unique integer

    Returns:
        tup (tuple): Tuple containing both integers

    See Also:
        :func:`~exa.jitted.szudzik_pairing`

    .. _Szudzik: http://szudzik.com/ElegantPairing.pdf
    '''
    a = np.int(szudzik_number - np.floor(np.sqrt(szudzik_number))**2)
    b = np.int(np.floor(np.sqrt(szudzik_number)))
    if a < b:
        return a, b
    else:
        return b, a - b


def map_x_to_y(x, y):
    '''
    Maps the values in x to that of y.

    Create a new array x mapping original values of x on the array y.
    For example, x may containing indices of interest of array y;
    the new array x will containing the values of interest from y. This
    function acts like a "dispatcher".

    Examples:
        >>> import numpy as np
        >>> x = np.array([0, 1, 5])
        >>> y = np.array([1, 2, 3, 4, 5, 10, 11])
        >>> map_x_to_y(x, y)
        array([ 1,  2, 10])

    Args:
        x (:class:`~numpy.ndarray`): Array of index values
        y (:class:`~numpy.ndarray`): Array of values to be used in mapping

    Returns:
        new (:class:`~numpy.ndarray`): Mapped result (of y typed elements)

    See Also:
        Conceptually similar to :func:`functools.singledispatch` and the
        related (but not - yet - standard) `multipledispatch`_ package.

    .. _multipledispatch: http://multiple-dispatch.readthedocs.org/en/latest/
    '''
    v = y[0]
    if isinstance(v, np.int32):
        return _map_x_to_y_int32(x, y)
    elif isinstance(v, np.int64):
        return _map_x_to_y_int64(x, y)
    elif isinstance(v, np.float32):
        return _map_x_to_y_float32(x, y)
    elif isinstance(v, np.float64):
        return _map_x_to_y_float64(x, y)
    else:
        raise TypeError('Unsupported type {0}'.format(type(v)))

@njit([int32[:](int32[:], int32[:]),
       int32[:](int64[:], int32[:])], cache=True)
def _map_x_to_y_int32(x, y):
    result = np.empty((len(x), ), dtype=int32)
    for i, v in enumerate(x):
        result[i] = y[v]
    return result

@njit([int64[:](int32[:], int64[:]),
       int64[:](int64[:], int64[:])], cache=True)
def _map_x_to_y_int64(x, y):
    result = np.empty((len(x), ), dtype=int64)
    for i, v in enumerate(x):
        result[i] = y[v]
    return result

@njit([float32[:](int32[:], float32[:]),
       float32[:](int64[:], float32[:])], cache=True)
def _map_x_to_y_float32(x, y):
    result = np.empty((len(x), ), dtype=float32)
    for i, v in enumerate(x):
        result[i] = y[v]
    return result

@njit([float64[:](int32[:], float64[:]),
       float64[:](int64[:], float64[:])], cache=True)
def _map_x_to_y_float64(x, y):
    result = np.empty((len(x), ), dtype=float64)
    for i, v in enumerate(x):
        result[i] = y[v]
    return result


######################################################################################################################################


@njit
def expand_array_values_int(values, n):
    '''
    Expands a list of unique values to a list of n repetitions of each
    unique value.

    Args
        values (:class:`~numpy.ndarray`): Numpy array values
        n (int): Inner count to expand by

    Returns
        array (:class:`~numpy.ndarray`): Expanded array

    .. code-block: Python

        a = [1, 2, 3]
        n = 2
        c = expand_array_values_int(a, n)
        print(c)   # prints "[1, 1, 2, 2, 3, 3]"
    '''
    nvalues = len(values)
    nn = nvalues * n
    expanded = np.empty((nn, ), dtype=int64)
    i = 0
    for value in values:
        for j in range(n):    # j is unused
            expanded[i] = value
            i += 1
    return expanded


@njit
def _exp_2_i8_v(values, bins, nn):
    '''
    Expands the array of values by the spacing given in the bins array,
    and returns both the expanded values and the array of zero based
    indexes corresponding to the bins.

    Args
        values (:class:`~numpy.ndarray`): Numpy array values
        bins (:class:`~numpy.ndarray`): Bins which define each n
        nn (int): Total length of the result

    Returns
        outer (:class:`~numpy.ndarray`): Expanded values array
        inner (:class:`~numpy.ndarray`): Expanded inner array

    Warning
        The bins argument must have length = len(values) + 1
        for this function to work. Assumes zero based indexing.

    See Also
        :func:`~exa.jitted.expand_array_values_int_variable`

    .. code-block: Python

        a = [1, 2, 3]
        bins = [0, 2, 4, 7]
        n = 7
        c, d = expand_array_values_int_variable(a, bins, n)
        print(c)   # prints "[1, 1, 2, 2, 3, 3, 3]"
        print(d)   # prints "[0, 1, 0, 1, 0, 1, 2]"
    '''
    n = len(values)
    outer = np.empty((nn, ), dtype=int64)
    inner = np.empty((nn, ), dtype=int64)
    k = 0
    for i in range(n):
        nnn = bins[i + 1] - bins[i] - 1    # Assumes zero based indexing
        for j in range(nnn):
            outer[k] = values[i]
            inner[k] = j
            k += 1
    return outer, inner




@njit
def expand3(array, bins):
    '''
    '''
    k = 0
    n = np.sum(bins)
    expanded = np.empty((n, 3), dtype=float64)
    for i, count in enumerate(bins):
        for j in range(count):
            expanded[k, :] = array[i]
            k += 1
    return expanded


@njit
def _expand3_single(vector, count):
    '''
    '''
    k = 0
    expanded = np.empty((count, 3), dtype=float64)
    for j in range(count):
        expanded[k, :] = vector
        k += 1
    return expanded


@njit
def reindex(original):
    '''
    Reindex the current frame index with complete fidelity.

    Args
        original (:class:`~numpy.ndarray`): Array to reindex

    Returns
        new (:class:`~numpy.ndarray`): Reindexed array
    '''
    n = len(original)
    new = np.empty((n, ), dtype=int64)
    previous = original[0]
    index = 0
    for i, current in enumerate(original):
        if previous == current:
            new[i] = index
        else:
            previous = current
            index += 1
            new[i] = index
    return new


# Vectorized functions
# Note that we numbafy these functions below based on system architecture
@vectorize(['float64(float64)'], nopython=True)
def psqrt(value):
    '''
    Performs the square root operation.

    .. code-block:: Python

        a = 100.0
        psqrt(a)    # returns 10.0
    '''
    return value ** 0.5

@vectorize(['float64(float64, float64)'], nopython=True)
def mod(x, y):
    '''
    Performs modulo operation.

    .. code-block:: Python

        a = 100.0
        mod(a, 9)    # returns 1
    '''
    return np.mod(x, y)


@vectorize(['float64(float64, float64)'], nopython=True)
def mul(x, y):
    '''
    Vectorized multiplication.

    .. code-block:: Python

        a = np.random.rand(10000000)
    '''
    return x * y


# Wrapper functions for the above pre-compiled functions
def euclid_dist(narr, threshold=20000):
    '''
    Computes the euclidean distance between all elements of an
    n by m dimensional array.

    Args
        narr (:class:`numpy.ndarray`): Numpy array of dimension n by m (rows by columns)
        threshold (int): If n is larger than this value will call parallel square root (optional)

    Returns
        dist (:class:`numpy.ndarray`): Numpy array of dimension (n * (n - 1) / 2) of distances

    Note
        This function is the vectorized square root of :func:`~exa.jitted.euclid_dist2`

    Warning
        This is a combinatorial operation!
    '''
    return psqrt(euclid_dist2(narr))
