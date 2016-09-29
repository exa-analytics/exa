# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Pairing Functions
####################
Pairing functions are used to map (bijectively: one-to-one) elements of tow sets.
"""
import numpy as np
from exa.compute.dispatch import dispatch


@dispatch((int, np.int64), (int, np.int64))
def cantor(k1, k2):
    """
    `Cantor`_ pairing function takes two numbers and creates a unique number.

    .. math::

        f\\left(k_1, k_2\\right) = \\frac{1}{2}\\left(k_1 + k_2\\right)
        \\left(k_1 + k_2 + 1\\right) + k_2

    Args:
        k1 (int): First number
        k2 (int): Second number

    Returns:
        k12 (int): Unique number based on k1, k2

    .. _Cantor: https://en.wikipedia.org/wiki/Pairing_function#Cantor_pairing_function
    """
    return int((k1 + k2)*(k1 + k2 + 1)//2 + k2)


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
    z = np.int64(z)
    w = np.floor((np.sqrt(8*z + 1) - 1)//2).astype(np.int64)
    t = (w**2 + w)//2
    y = z - t
    x = w - y
    return x, y


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
        return np.int64(y**2 + x)
    return np.int64(x**2 + x + y)


def invert_szudzik(z):
    """
    From a Szudzik number, extract the input values of x and y.

    See Also:
        :func:`~exa.compute.algorithms.pairing.szudzik`
    """
    z = np.int64(z)
    w = np.floor(np.sqrt(z)).astype(np.int64)
    t = z - w**2
    if t < w:
        return t, w
    return w, t - w


def unordered(x, y):
    """
    Pairing function for to elements where order doesn't matter.

    .. math::

        \\left(x, y\\right) = xy + trunc\\left[\\left(\\left|x - y\\right|
        - 1\\right)^2/4\\right] = \\left(y, x\\right)
    """
    return x*y + np.trunc((np.abs(x - y) - 1)**2/4).astype(np.int64)
