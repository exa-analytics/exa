# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Units and Conversions
############################
Custom units built atop of `sympy`_'s dimension and unit system infrastructure.
Units can be accessed directly at the module level.

.. code-block:: Python

    au = exa.units.atomic_time
    au   # prints '2.4188..E-17*s'
    m = exa.units.m
    m    # prints 'm'

Units can be assigned to Exa's data objects: see :mod:`~exa.core.dataseries`.
This module also provides common prefixes (e.g. 'kilo') via `sympy`_.

.. _sympy: http://www.sympy.org/en/index.html
"""
import sympy
import sympy.physics
units = []
for name, value in vars(sympy.physics.units).items():
    if isinstance(value, (sympy.physics.units.Unit, sympy.Mul, sympy.Rational)):
        units.append(name)
# Dynamically generate import list
sympy.physics.units.__all__ = units
from sympy.physics.units import *


# Lengths
atomic_length = 5.2917721092E-11*m


# Times
atomic_time = 2.418884326505E-17*s


# Energies
hartree = 4.35974434E-18*joule
rydberg = 13.605693009*eV


# Cleanup the namespace
del sympy, units
