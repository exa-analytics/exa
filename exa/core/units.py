# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Quantity Support
#########################
Exa has a concept for a quantity, a number with associated units. This is
accomplished by leveraging Sympy's `unitsystem`_ interface. Quantities can be
used to define a single value or attached to data objects (such as a
:class:`~exa.core.discrete.Series` or :class:`~exa.core.discrete.DataFrame`).

.. _unitsystem: http://docs.sympy.org/dev/modules/physics/unitsystems/units.html
"""
from sympy.physics import units as _units


class Unit(_units.Unit):
    """Units for data objects."""
    def __add__(self, other):
        u0 = self.as_coeff_Mul()
        u1 = self.as_coeff_Mul()
        if u0[1] == u1[1]:
            pass
