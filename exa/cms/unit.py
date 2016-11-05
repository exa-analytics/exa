# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Unit Conversions
#########################
This module provides relational classes for unit conversion tables. To inspect
available conversions:

.. code-block: Python

    exa.cms.unit.Length.to_frame()    # display full conversion table
    exa.cms.unit.Length.units()       # list available units

To create a new conversion:

.. code-block: Python

    exa.cms.unit.Dimension.create("kJ", "J", 1000)   # Note create J -> kJ too

For high performance use the cached conversion factors directly:

.. code-block: Python

    exa.cms.unit.units[("kJ", "J")]
"""
import six
from sqlalchemy import and_, String, Float, Column
from exa.cms.base import BaseMeta, Base, scoped_session


class Meta(BaseMeta):
    """
    Special metaclass for unit objects supporting aliases. Aliases are
    alternative names for standard symbols for units.
    """
    aliases = {}     # Note that all aliases should be lowercase (see below)
    def _getitem(cls, key):
        if isinstance(key, tuple):
            f = cls.aliases[key[0].lower()] if key[0].lower() in cls.aliases else key[0]
            t = cls.aliases[key[1].lower()] if key[1].lower() in cls.aliases else key[1]
            with scoped_session() as session:
                return session.query(cls).filter(and_(cls.from_unit==f, cls.to_unit==t)).one().factor
        else:
            raise KeyError('Usage requires syntax Dimension["from_unit", "to_unit"]')


class Dimension(object):
    """
    Descriptive class for units.

    Attributes:
        from_unit (str): Unit to convert from
        to_unit (str): Unit to convert to
        factor (float): Conversion factor
    """
    from_unit = Column(String(8), nullable=False)
    to_unit = Column(String(8), nullable=False)
    factor = Column(Float, nullable=False)

    @classmethod
    def units(cls):
        return sorted(cls.to_frame()['to_unit'].unique())

    @classmethod
    def create(cls, from_unit, to_unit, factor):
        with scoped_session() as session:
            obj0 = cls(from_unit=from_unit, to_unit=to_unit, factor=factor)
            obj1 = cls(from_unit=to_unit, to_unit=from_unit, factor=1/factor)
            session.add(obj0)
            session.add(obj1)
        reconfigure_units()


class Length(six.with_metaclass(Meta, Base, Dimension)):
    """
    Length conversions.

        >>> Length['angstrom', 'au']
        1.88971616463
        >>> Length['A', 'au']
        1.88971616463
        >>> Length['A', 'a0']
        1.88971616463
    """
    aliases = {
        'a.u.': 'au',
        'bohr': 'au',
        'angstrom': 'A',
        'angstroms': 'A',
        u'\u212B': 'A',
        u'\u212Bngstrom': 'A',
        'a0': 'au'
    }


class Mass(six.with_metaclass(Meta, Base, Dimension)):
    """
    >>> Mass['kg', 'lb']
    2.2046226218
    >>> Mass['Da', 'kg']
    1.660538921000011e-27
    >>> Mass['u', 'kg']
    1.660538921000011e-27
    """
    aliases = {
        'amu': 'u',
        'au': 'u'
    }


class Time(six.with_metaclass(Meta, Base, Dimension)):
    """
    >>> Time['min', 's']
    60.0000000000024
    >>> Time['hr', 's']
    3599.999712000023
    >>> Time['weeks', 'days']
    6.999999999955003
    """
    pass


class Current(six.with_metaclass(Meta, Base, Dimension)):
    """
    >>> Current['A', 'C_s']
    1.0
    >>> Current['A', 'Bi']
    0.1
    """
    pass


class Amount(six.with_metaclass(Meta, Base, Dimension)):
    """
    >>> Amount['gmol', 'mol']
    1.0
    >>> Amount['lbmol', 'mol']
    453.5923744952991
    """
    pass


class Luminosity(six.with_metaclass(Meta, Base, Dimension)):
    """
    >>> Luminosity['cp', 'cd']
    0.9810000000433602
    """
    pass


class Dose(six.with_metaclass(Meta, Base, Dimension)):
    """
    >>> Dose['Gy', 'rd']
    100.0
    >>> Dose['J_kg', 'rd']
    100.0
    """
    pass


class Acceleration(six.with_metaclass(Meta, Base, Dimension)):
    """
    >>> Acceleration['m_s2', 'cm_s2']
    100.0
    >>> Acceleration['m_s2', 'stdgrav']
    0.10197162130000001
    """
    pass


class Charge(six.with_metaclass(Meta, Base, Dimension)):
    """
    >>> Charge['e', 'C']
    1.6021765649999947e-19
    """
    pass


class Dipole(six.with_metaclass(Meta, Base, Dimension)):
    """
    >>> Dipole['yCm', 'D']
    299792.45817809016
    """
    pass


class Energy(six.with_metaclass(Meta, Base, Dimension)):
    """
    >>> Energy['J', 'cal']
    0.2388458966
    >>> Energy['kcal', 'Btu']
    3.9683205782473134
    """
    aliases = {
        'cm-1': 'cm^-1'
    }


class Force(six.with_metaclass(Meta, Base, Dimension)):
    """
    >>> Force['N', 'lbf']
    0.22480894310000002
    """
    pass


class Frequency(six.with_metaclass(Meta, Base, Dimension)):
    """
    >>> Frequency['1_s', 'Hz']
    1.0
    """
    pass


class MolarMass(six.with_metaclass(Meta, Base, Dimension)):
    """
    >>> MolarMass['g_mol', 'kg_mol']
    0.001
    """
    pass


def reconfigure_units():
    """Update unit (:attr:`~exa.cms.unit.units`) conversion factors."""
    global units
    units = {}
    for unit in unit_tables:
        series = unit.to_frame().set_index(['from_unit', 'to_unit'])['factor']
        units.update(series.to_dict())


unit_tables = [Length, Mass, Time, Current, Amount, Luminosity, Dose, Acceleration,
               Charge, Dipole, Energy, Force, Frequency, MolarMass]
units = None
reconfigure_units()
