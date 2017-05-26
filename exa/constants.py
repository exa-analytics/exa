# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Physical Constants
#######################################
Physical constant data comes from `NIST`_. Numerical values, error, and units
are included for each constant. By default, values are given in the units the
are listed in.

.. code-block:: python

    from exa import constants
    constants.Hartree_energy          # 4.35974465e-18
    constants.Hartree_energy.value    # 4.35974465e-18
    constants.Hartree_energy.error    # 5.4e-26
    constants.Hartree_energy.units    # 'J'

.. _NIST: http://physics.nist.gov/cuu/Constants/Table/allascii.txt
"""
import six
import os as _os
import sys as _sys
from pkg_resources import resource_filename as _resource_filename
from exa import _datadir
from .single import Singleton as _Singleton
from .core.editor import Editor as _Editor


class Constant(_Singleton):
    """
    By inheriting the :class:`~exa.single.Singleton` class directly, this object
    is in fact a singleton factory.
    """
    def __new__(mcs, name, bases, clsdict):
        mcs.__repr__ = lambda self: repr(self.value)
        return super(Constant, mcs).__new__(mcs, name, bases, clsdict)


def _create():
    """Generate the isotopes and elements API from their static data."""
    lst = _Editor(_path).to_data('json')
    for entry in lst:
        name = str(entry['name'])
        setattr(_this, name, Constant(name, (), entry))


# Data order of isotopic (nuclear) properties:
_this = _sys.modules[__name__]
_resource = "constants.json.bz2"
_path = _resource_filename(_datadir()[0], _os.path.join(_datadir()[1], _resource))
if not hasattr(_this, "a220_lattice_spacing_of_silicon"):
    _create()
