# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Periodic Table of Elements and Isotopes
########################################
This module provides a database of the atomic elements and their isotopes.
Visualization parameters are also provided. Data is provided and maintained
by `NIST`_. The full api is given in the code example below. Note that not
all attributes that are present on isotopes are present on elements (and vice
versa).

.. code-block:: python

    from exa.util import isotopes
    isotopes.H            # Hydrogen element
    isotopes.H[2]         # Hydrogen isotopes 2 (deuterium)
    isotopes.H.radius     # Empirical covalent radius (a.u. - Bohr)
    isotopes.H.af         # Abundance fraction
    isotopes.H.afu        # Abundance fraction uncertainty
    isotopes.H.mass       # Atomic mass (g/mol)
    isotopes.H.massu      # Atomic mass uncertainty (g/mol)
    isotopes.H.eneg       # Electronegativity (Pauling scale)
    isotopes.H[2].quad    # Nuclear quadrupole moment (eb - electron-barn - e10^(-28)m^2)
    isotopes.H[2].A       # Atomic mass number (g/mol)
    isotopes.H.Z          # Proton number
    isotopes.H[2].g       # Nuclear g-factor (dimensionless magnetic moment)
    isotopes.H[2].spin    # Nuclear spin
    isotopes.H.color      # Traditional atomic color (HTML)
    isotopes.H.name       # Full element name

Warning:
    Isotopes are provided as part of the static data directory.

.. _NIST: https://www.nist.gov/
"""
import json as _json
import six as _six
import sys as _sys
from exa import Editor as _E
from exa import DataFrame as _DF
from exa.static import resource as _resource


class Element(object):
    """
    An element from Mendeleev's periodic table.

    .. code-block:: python

        from exa.util import isotopes
        H = isotopes.H         # Hydrogen element (isotope averaged)
        D = isotopes.H[2]      # Deuterium (2H, a specific isotope)
        isotopes.H.isotopes    # List of available isotopes
    """
    @property
    def isotopes(self):
        return [v for k, v in vars(self).items() if k.startswith("_")]

    def __init__(self, symbol, name, mass, znum, radius, color):
        self.symbol = symbol
        self.name = name
        self.mass = mass
        self.Z = znum
        self.radius = radius
        self.color = color

    def __getitem__(self, key):
        if isinstance(key, _six.integer_types):
            return getattr(self, "_"+str(key))
        return getattr(self, key)

    def __repr__(self):
        return "{}({}, {})".format(self.symbol, self.Z, self.mass)


class Isotope(object):
    """
    A specific atomic isotope (the physical manifestation of an element).

    .. code-block:: python

        from exa.util import isotopes
        u235 = isotopes.U[235]    # Specific isotope of Uranium
        u235.mass                 # Mass of 235 U isotope

    Attributes:
        A (int): Mass number
        Z (int): Proton number
        af (float): Abundance fraction
        afu (float): Abundance fraction uncertainty
        radius (float): Colvalent radius (approximate)
        g (float): Nuclear g-factor
        mass (float): Atomic mass (in g/mol)
        massu (float): Atom mass uncertainty
        name (str): Full name
        eneg (float): Electronegativity (Pauling scale
        quad (float): Nuclear quadrupole moment (electron-barn units)
        spin (float): Nuclear spin
        symbol (str): Element symbol
        color (str): Color as hexidecimal string
    """
    def __init__(self, anum, znum, af, afu, radius, g, mass, massu, name,
                 eneg, quad, spin, symbol, color):
        self.A = anum
        self.Z = znum
        self.af = af
        self.afu = afu
        self.radius = radius
        self.g = g
        self.mass = mass
        self.massu = massu
        self.name = name
        self.eneg = eneg
        self.quad = quad
        self.spin = spin
        self.symbol = symbol
        self.color = color

    def __repr__(self):
        return "{}({}, {})".format(self.symbol, self.A, self.Z)


def _create():
    """Globally called function for creating the isotope/element API."""
    def creator(group):
        """Helper function applied to each symbol group of the raw isotope table."""
        symbol = group['symbol'].values[0]
        try:    # Ghosts and custom atoms don't necessarily have an abundance fraction
            mass = (group['mass']*group['af']).sum()/group['af'].sum()
        except ZeroDivisionError:
            mass = group['mass'].mean()
        znum = group['Z'].max()
        radius = group['radius'].mean()
        try:
            color = group.loc[group['af'].idxmax(), 'color']
        except TypeError:
            color = group['color'].values[0]
        name = group['name'].values[0]
        ele = Element(symbol, name, mass, znum, radius, color)
        # Attached isotopes
        for tope in group.apply(lambda s: Isotope(*s.tolist()), axis=1):
            setattr(ele, "_"+str(tope.A), tope)
        return ele

    iso = _DF(_json.loads(str(_E(_path))), columns=_columns)
    for element in iso.groupby("symbol").apply(creator):
        setattr(_this, element.symbol, element)


def _df():
    """Return a dataframe of isotopes."""
    records = []
    for sym, ele in vars(_this).items():
        if sym not in ["Element", "Isotope"] and not sym.startswith("_"):
            for k, v in vars(ele).items():
                if k.startswith("_") and k[1].isdigit():
                    records.append({kk: vv for kk, vv in vars(v).items() if not kk.startswith("_")})
    return _DF.from_records(records)


def get(key):
    """
    Retrieve an element by symbol or by proton number (Z).

    .. code-block:: python

        isotopes.get(92)
        isotopes.get("U")
        isotopes.get("h")    # Corrects lowercase
    """
    if isinstance(key, _six.integer_types):
        key = df.loc[df['Z'] == key, 'symbol'].values[0]
    return getattr(_this, key.title())


# Data order of isotopic (nuclear) properties:
_columns = ("A", "Z", "af", "afu", "radius", "g", "mass", "massu", "name",
            "eneg", "quad", "spin", "symbol", "color")
_this = _sys.modules[__name__]         # Reference to this module
_path = _resource("isotopes.json.bz2")
if not hasattr(_this, "H"):
    _create()
    df = _df()
