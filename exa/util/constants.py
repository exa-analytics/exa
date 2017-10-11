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
#import os as _os
#import sys as _sys
#from json import loads as _loads
#from exa import Editor as _E
#from exa import DataFrame as _DF
#from exa.util.units import get as _get
#
#
#class Constant(float):
#    """A physical constant."""
#    def __new__(cls, value, name, units, error):
#        return super(Constant, cls).__new__(cls, value)
#
#    def __init__(self, value, name, units, error):
#        float.__init__(value)
#        self.name = name
#        self.units = _get(units)
#        self.error = error
#
#
#def _create():
#    """Generate physical constants from static data."""
#    for entry in _loads(str(_E(_path))):
#        name = entry['name']
#        value = entry['value']
#        units = entry['units']
#        error = entry['error']
#        setattr(_this, name, Constant(value, name, units, error))
#
#
## Data order of isotopic (nuclear) properties:
#_resource = "../../static/constants.json.bz2"
#_this = _sys.modules[__name__]
#_path = _os.path.abspath(_os.path.join(_os.path.abspath(__file__), _resource))
#if not hasattr(_this, "a220_lattice_spacing_of_silicon"):
#    _create()
