# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Unit Conversions
########################################
Values are reported with respect to the base SI unit for a given quantity.
Conversion factors can be generated using the syntax, Quantity[from, to];
see the example below.

.. code-block:: python

    from exa.util.units import Energy
    Energy.values        # Check available symbols
    Energy["eV"]         # Value of eV in SI units
    Energy["eV", "J"]    # Same as above
    Energy["eV", "Ha"]   # Conversion factor between eV and Ha (Hartree atomic unit)
"""
import sys as _sys
import six as _six
import numpy as _np
import pandas as _pd
import json as _json
from exa import Editor as _Editor
from exa.static import resource as _resource


class Unit(object):
    """
    A quantity with given (named) dimensions whose value is presented relative
    to the corresponding SI value.

    .. code-block:: python

        Unit.values         # Check available symbols
        Unit[key]           # Return value of key relative to SI
        Unit[key0, key1]    # Return conversion from key0 to key1
    """
    @property
    def values(self):
        return self._values

    def __setitem__(self, key, value):
        self._values[key] = value

    def __getitem__(self, key):
        if isinstance(key, _six.string_types):
            k = self._values[_np.isclose(self._values, 1.0)].index[0]
            return self._values[k]/self._values[key]
        elif isinstance(key, (list, tuple)):
            return self._values[key[1]]/self._values[key[0]]

    def __init__(self, values, name):
        self._values = _pd.Series(values)
        self._name = name


def _create():
    def creator(name, data):
        data.pop("dimensions", None)
        data.pop("aliases", None)
        return Unit(data, name)

    dct = _json.load(_Editor(_path).to_stream())
    for name, data in dct.items():
        setattr(_this, name.title(), creator(name, data))


_this = _sys.modules[__name__]         # Reference to this module
_path = _resource("units.json.bz2")
if not hasattr(_this, "Energy"):
    _create()
