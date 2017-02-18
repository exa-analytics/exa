# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Pairing Functions
####################
Pairing functions are used to map (bijectively: one-to-one) elements of tow sets.
"""
import numpy as np
from exa.compute.dispatcher import dispatch, ints


@dispatch(ints, ints)
def cantor(x, y):
    """
    `Cantor`_ pairing function takes two numbers and creates a unique number.

    .. math::

        f\\left(x, y\\right) = \\frac{1}{2}\\left(x + y\\right)
        \\left(x + y + 1\\right) + y

    Args:
        x (int): First number
        y (int): Second number

    Returns:
        x2 (int): Unique number based on x, y

    .. _Cantor: https://en.wikipedia.org/wiki/Pairing_function#Cantor_pairing_function
    """
    return int((x + y)*(x + y + 1)//2 + y)


@dispatch(ints)
def invert_cantor(z):
    """
    Extract the input numbers for a given :func:`~exa.compute.algorithms.pairing.cantor`
    result.

    .. math::

        w &= \\left\\lfloor{\\frac{\\sqrt{8z + 1} - 1}{2}}\\right\\rfloor \\\\
        t &= \\frac{w^2 + w}{2} \\\\
        y &= z - t \\\\
        x &= w - y \\\\

    Args:
        z: Cantor function result

    Returns:
        (k1, k2): Cantor pairs
    """
    w = np.floor((np.sqrt(8*z + 1) - 1)//2)
    t = (w**2 + w)//2
    y = z - t
    x = w - y
    return int(x), int(y)


@dispatch(ints, ints)
def szudzik(x, y):
    """
    `Szudzik`_ pairing function.

    .. math::

        f\\left(x, y\\right) = \\begin{cases}
        x + y^2\ &if x < y \\\\
        x^2 + x + y\ &otherwise \\\\
        \\end{cases}

    See Also:
        http://stackoverflow.com/questions/919612/mapping-two-integers-to-one-in-a-unique-and-deterministic-way

    .. _Szudzik: http://szudzik.com/ElegantPairing.pdf
    """
    if x < y:
        return int(y**2 + x)
    return int(x**2 + x + y)


@dispatch(ints)
def invert_szudzik(z):
    """
    From a Szudzik number, extract the input values of x and y.

    Args:
        z (int): Szudzik number

    Returns:
        xy (tuple): Input x, y pair (as ints)

    See Also:
        :func:`~exa.compute.algorithms.pairing.szudzik`
    """
    w = np.floor(np.sqrt(z))
    t = z - w**2
    if t < w:
        return int(t), int(w)
    return int(w), int(t - w)


@dispatch(ints, ints)
def unordered(x, y):
    """
    The :func:`~exa.compute.algorithms.pairing.szudzik` pairing function
    ordered such that the first argument is greater than the second argument.
    """
    if x > y:
        return szudzik(x, y)
    return szudzik(y, x)


@dispatch(ints)
def invert_unordered(z):
    """
    Invert :func:`~exa.compute.algorithms.pairing.unordered` to return input
    arguments (ordered in descending order).
    """
    x, y = invert_szudzik(z)
    if x > y:
        return x, y
    return y, x
