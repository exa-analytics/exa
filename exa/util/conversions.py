# -*- coding: utf-8 -*-
# Copyright (c) 2015-2020, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Common conversion factors
##########################################
Conversion factors from the tabulated physical constants from `NIST`_.
All of the entries that end with relationship are taken to be the conversion
units provided by `NIST`_ and they are listed by a hardcoded acronym value.

.. code-block:: python

    >>> conversions.Ha2eV
    27.211386245988002
    >>> conversions.Ha2eV.error
    5.3e-11
    >>> conversions.Ha2inv_m
    21947463.13632
"""
import sys as _sys
import pandas as _pd
from exa.static import resource as _resource


class Conversion(float):
    """
    Conversion factors taken from the NIST constants table. Only those
    that end with relationship are taken to be the conversion factors.

    Acronyms are as follows:

    - 'u': Unified atomic mass unit (Dalton)
    - 'amu': Atomic unit of mass
    - 'eV': Electron volt
    - 'J': Joule
    - 'Ha': Hartree
    - 'inv_m': Inverse meter
    - 'K': Kelvin
    - 'Kg': Kilogram
    - 'Hz': Hertz
    """
    def __new__(cls, name, units, value, error):
        return super(Conversion, cls).__new__(cls, value)

    def __init__(self, name, units, value, error):
        float.__init__(value)
        self.name = name
        self.units = units
        self.error = error
        self.value = value

def _get_acronym(name):
    mapper = {'atomic_mass_unit': 'u', 'electron_volt': 'eV', 'joule': 'J',
              'hartree': 'Ha', 'inverse_meter': 'inv_m', 'kelvin': 'K',
              'kilogram': 'Kg', 'hertz': 'Hz'}
    key = ['', '2', '']
    for unit, acr in mapper.items():
        if name.startswith(unit):
            key[0] = acr
        elif name.endswith(unit+'_relationship'):
            key[2] = acr
        elif name == 'electron_mass':
            key = 'amu2Kg'
        elif name == 'electron_mass_in_u':
            key = 'amu2u'
    if ''.join(key) == '2':
        raise ValueError("Could not determine the acronym for the value {}".format(name))
    return ''.join(key)

def _create():
    alt_conversions = ['electron_mass', 'electron_mass_in_u']
    df = _pd.read_csv(_path)
    for quan, unit, err, val in zip(df['quantity'], df['unit'],
                                    df['uncertainty'], df['value']):
        if quan.endswith('relationship') or quan in alt_conversions:
            name = _get_acronym(quan)
            setattr(_this, name, Conversion(name=name, units=unit, value=val,
                                            error=err))

_this = _sys.modules[__name__]
_path = _resource("nist-constants-2018.csv")
if not hasattr(_this, "Planck_constant"):
    _create()

