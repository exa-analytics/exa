# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Quantities
############################
This module provides :class:`~exa.util.quantity.Quantity` objects. These
objects are the base class for numbers which have associated units.
"""


class Quantity(object):
    """Base class for quantities."""
    def __repr__(self):
        value = super(Quantity, self).__repr__()
        return "{} {}".format(value, self.unit)


class FloatQuantity(Quantity, float):
    """A floating point number with associated units."""
    def __new__(cls, value, unit, name=None, description=None):
        return super(FloatQuantity, cls).__new__(cls, value)

    def __init__(self, value, unit, name=None, description=None):
        float.__init__(value)
        self.unit = unit
        self.name = name
        self.description = description
