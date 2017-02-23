# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Elements and Isotopes
#########################
This module creates elements and isotopes. Isotopes take the form of
element symbol followed by mass number (e.g. ``H1``) while elements are
simply ``H``. Static isotope data is stored in the 'data' directory.
"""
import os as _os
import sys as _sys
from pkg_resources import resource_filename as _resource_filename
from numpy import nan as _nan
from exa.single import Singleton as _Singleton
from exa.editor import Editor as _Editor


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
        mcs.af = property(lambda cls: cls.abundance_fraction)
        mcs.afe = property(lambda cls: cls.abundance_fraction_error)
        mcs.rad = property(lambda cls: cls.covalent_radius)
        mcs.masse = property(lambda cls: cls.mass_error)
        mcs.eneg = property(lambda cls: cls.electronegativity)
        mcs.quad = property(lambda cls: cls.quadrupole_moment)
        return super(_Element, mcs).__new__(mcs, name, bases, clsdict)


def _create():
    """Generate the isotopes and elements API from their static data."""
    def create_isotope_attr(tope):
        """Helper function to create an isotope attribute."""
        dct = tope.to_dict()
        attrname = dct['symbol'] + str(dct['A'])
        isotope = _Isotope(attrname, (), dct)
        setattr(_this, attrname, isotope)

    # Start processing isotopes
    isotopes = _Editor(_path).to_data('pdjson')
    isotopes.columns = _columns
    for name, group in isotopes.groupby('name'):
        group.apply(create_isotope_attr, axis=1)
        element = {'name': name, 'Z': group['Z'].values[0],
                   'color': group['color'].values[0],
                   'symbol': group['symbol'].values[0],
                   'electronegativity': group['electronegativity'].values[0],
                   'covalent_radius': group['covalent_radius'].values[0]}
        element['mass'] = (group['abundance_fraction']*group['mass']).sum()
        element = _Element(element['symbol'], (), element)
        setattr(_this, element.symbol, element)


# Data order of isotopic (nuclear) properties:
_columns = ['A', 'Z', 'abundance_fraction', 'abundance_fraction_error',
            'covalent_radius', 'g_factor', 'mass', 'mass_error', 'name',
            'electronegativity', 'quadrupole_moment', 'spin', 'symbol',
            'color']
_this = _sys.modules[__name__]         # Reference to this module
#_path = _os.path.join(_os.path.split(__file__)[0], "../data/isotopes.json.bz2")
_path = _resource_filename("exa", "data/isotopes.json.bz2")
if not hasattr(_this, "H"):
    _create()

