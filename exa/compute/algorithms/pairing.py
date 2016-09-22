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


def cantor(k1, k2):
    """
    `Cantor`_ pairing function takes two numbers and creates a unique number.

    .. math::

        f\\left(k_1, k_2\\right) = \\frac{1}{2}\\left(k_1 + k_2\\right)
        \\left(k_1 + k_2 + 1\\right) + k_2

    Args:
        k1: First number
        k2: Second number

    Returns:
        k12: Unique number based on k1, k2

    .. _Cantor: https://en.wikipedia.org/wiki/Pairing_function#Cantor_pairing_function
    """
    return (k1 + k2)*(k1 + k2 + 1)//2 + k2


def invert_cantor(z):
    """
    Extract the input numbers for a given :func:`~exa.compute.algorithms.pairing.cantor`
    result.

    .. math::

        w = \\left\\lfloor{\\frac{\\sqrt{8z + 1} - 1}{2}}\\right\\rfloor \\\\
        t = \\frac{w^2 + w}{2} \\\\
        y = z - t \\\\
        x = w - y \\\\

    Args:
        z: Cantor function result

    Returns:
        k1: First number in Cantor pair
        k2: Second number in Cantor pair
    """
    w = np.floor((np.sqrt(8*z + 1) - 1)//2).astype(np.int64)
    t = (w**2 + w)//2
    y = z - t
    x = w - y
    return x, y


def szudzik(x, y):
    """
    `Szudzik`_ pairing function.

    .. _Szudzik: http://szudzik.com/ElegantPairing.pdf

    See Also:
        http://stackoverflow.com/questions/919612/mapping-two-integers-to-one-in-a-unique-and-deterministic-way
    """
        xx = 2*x
    if x < 0:
        xx = -2*x - 1
    yy = 2*y
    if y < 0:
        yy = -2*y - 1
    if xx > yy:
        return y**2 + x
    return x**2 + x + y
