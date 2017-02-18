# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Elements and Isotopes
#########################
This modules stores isotope data.
"""
import sys as _sys
from numpy import nan as _nan
from exa.single import Singleton as _Singleton


class _Isotope(_Singleton):
    """A metaclass for creating isotopes - not an isotope itself."""
    def __new__(mcs, name, bases, clsdict):
        """Sets up some convenience aliases for various attributes."""
        mcs.isotope = property(lambda cls: cls.__name__)
        mcs.af = property(lambda cls: cls.abundance_fraction)
        mcs.afe = property(lambda cls: cls.abundance_fraction_error)
        mcs.rad = property(lambda cls: cls.covalent_radius)
        mcs.masse = property(lambda cls: cls.mass_error)
        mcs.eneg = property(lambda cls: cls.electronegativity)
        mcs.quad = property(lambda cls: cls.quadrupole_moment)
        return super(_Isotope, mcs).__new__(mcs, name, bases, clsdict)


class _Element(_Singleton):
    """A metaclass for creating elements - not an element itself."""
    def __new__(mcs, name, bases, clsdict):
        return super(_Element, mcs).__new__(mcs, name, bases, clsdict)


def _create():
    """Generate the isotopes and elements API from their static data."""
    for name, symbol, isotopes in _isotopes:
        element = {'name': name, 'symbol': symbol}
        for isotope in isotopes:
            dct = {_names[i]: datum for i, datum in enumerate(isotope)}
            dct.update(element)
            iso = _Isotope(symbol + str(dct['A']), (), dct)
            setattr(_this, iso.isotope, iso)
        element = _Element(symbol, (), element)
        setattr(_this, symbol, element)


# Data order of isotopic (nuclear) properties:
_names = ('A', 'Z', 'abundance_fraction', 'abundance_fraction_error', 'color',
          'covalent_radius', 'g_factor', 'mass', 'mass_error',
          'electronegativity', 'quadrupole_moment', 'spin')
_isotopes = (
    ("Hydrogen", "H", (
        (1, 1, 0.999855, 7e-7, '#9b9b9b',
         0.60471232, 5.5856912, 1.0078250321, 0.0,
         2.1, 0.0, 0.5), )
    ),
    ("Helium", "He", (
        (4, 2, 0.9999982, 3e-10, '#ffffd9',
         0.86927396, 0.0, 4.0026032542, 0.0,
         _nan, 0.0, 0.0), )
    )
)


_this = _sys.modules[__name__]    # Reference to this module
_create()
