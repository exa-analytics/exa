# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Units and Unit Conversions
############################
This module provides a database of units and mechanisms for interconversion
between units.

.. code-block:: python

    from exa.util import units
    units.m    # SI meter
"""
import six as _six
import os as _os
import sys as _sys
from json import loads as _loads
from exa import Editor as _E
from exa import DataFrame as _DF


class Derived(object):
    """
    A secondary or derived unit (e.g. acceleration).

    .. code-block:: python

        from exa.util import units
        units.acceleration.dimensions    # {'length': 1, 'time': -2, etc.}
        units.acceleration.m_s2          # meters/second^2

    """
    def __init__(self, name, length=0, mass=0, time=0, current=0,
                 temperature=0, amount=0, luminosity=0):
        self.name = name
        self.dimensions = {'length': length, 'mass': mass, 'time': time,
                           'current': current, 'temperature': temperature,
                           'amount': amount, 'luminosity': luminosity}


class Unit(float):
    """
    A unit with dimensions and values.
    """
    def __new__(cls, value, name, category, dimensions):
        return super(Unit, cls).__new__(cls, value)

    def __init__(self, value, name, category, dimensions):
        float.__init__(value)
        self.name = name
        self.category = category
        self.dimensions = dimensions


def _create():
    """Generate units from static data."""
    def creator(units, category):
        """Helper to create categories of units."""
        derived = Derived(category, **units['dimensions'])
        for name, value in units.items():
            if name in ("dimensions", "aliases"):
                continue
            setattr(derived, name, Unit(value, name, category,
                                        derived.dimensions))
        return derived

    dct = _loads(str(_E(_path)))
    for category, units in dct.items():
        setattr(_this, category, creator(units, category))


def get(name):
    """
    Get a unit with the given name.

    Args:
        name (str): Unit name

    Returns:
        unit (:class:`~exa.util.unit.Unit`): Returns the unit

    Warning:
        If not unit with the given name is found, none is returned.
    """
    # First try to get by simple name
    for derived in vars(_this).values():
        if isinstance(derived, Derived):
            for key, value in vars(derived).items():
                if key == name:
                    return value
    return None


# Data order of isotopic (nuclear) properties:
_resource = "../../static/units.json.bz2"
_this = _sys.modules[__name__]
_path = _os.path.abspath(_os.path.join(_os.path.abspath(__file__), _resource))
if not hasattr(_this, "s"):
    _create()
