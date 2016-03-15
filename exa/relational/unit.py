# -*- coding: utf-8 -*-
'''
Units and Dimensions
===============================================
This module provides relational classes for unit conversion tables.
'''
from sqlalchemy import and_, String, Float, Column
from exa.relational.base import BaseMeta, Base, session_scope


class _Meta(BaseMeta):
    aliases = {}

    def _getitem(cls, key):
        '''
        Support is provided for common unit aliases.
        '''
        if isinstance(key, tuple):
            f = cls.aliases[key[0]] if key[0] in cls.aliases else key[0]
            t = cls.aliases[key[1]] if key[1] in cls.aliases else key[1]
            factor = None
            with session_scope() as session:
                factor = session.query(cls).filter(and_(cls.from_unit==f, cls.to_unit==t)).one().factor
            return factor
        else:
            raise TypeError('Usage requires syntax Class["from_unit", "to_unit"]')


class Dimension:
    '''
    Generic class for physical dimension conversions. Doesn't do anything
    by itself but is inherited by specific dimension classes.

    Attributes:
        from_unit (str): Unit to convert from
        to_unit (str): Unit to convert to
        factor (float): Conversion factor
    '''
    from_unit = Column(String(8), nullable=False)
    to_unit = Column(String(8), nullable=False)
    factor = Column(Float, nullable=False)


class Length(Base, Dimension, metaclass=_Meta):
    '''
    >>> Length['angstrom', 'au']
    1.88971616463
    >>> Length['A', 'au']
    1.88971616463
    >>> Length['A', 'a0']
    1.88971616463
    '''
    aliases = {
        'bohr': 'au',
        'angstrom': 'A',
        u'\u212B': 'A',
        u'\u212Bngstrom': 'A',
        'a0': 'au'
    }


class Mass(Base, Dimension, metaclass=_Meta):
    '''
    >>> Mass['kg', 'lb']
    2.2046226218
    >>> Mass['Da', 'kg']
    1.660538921000011e-27
    >>> Mass['u', 'kg']
    1.660538921000011e-27
    '''
    pass


class Time(Base, Dimension, metaclass=_Meta):
    '''
    >>> Time['min', 's']
    60.0000000000024
    >>> Time['hr', 's']
    3599.999712000023
    >>> Time['weeks', 'days']
    6.999999999955003
    '''
    pass


class Current(Base, Dimension, metaclass=_Meta):
    '''
    >>> Current['A', 'C_s']
    1.0
    >>> Current['A', 'Bi']
    0.1
    '''
    pass


class Amount(Base, Dimension, metaclass=_Meta):
    '''
    >>> Amount['gmol', 'mol']
    1.0
    >>> Amount['lbmol', 'mol']
    453.5923744952991
    '''
    pass


class Luminosity(Base, Dimension, metaclass=_Meta):
    '''
    >>> Luminosity['cp', 'cd']
    0.9810000000433602
    '''
    pass


class Dose(Base, Dimension, metaclass=_Meta):
    '''
    >>> Dose['Gy', 'rd']
    100.0
    >>> Dose['J_kg', 'rd']
    100.0
    '''
    pass


class Acceleration(Base, Dimension, metaclass=_Meta):
    '''
    >>> Acceleration['m_s2', 'cm_s2']
    100.0
    >>> Acceleration['m_s2', 'stdgrav']
    0.10197162130000001
    '''
    pass


class Charge(Base, Dimension, metaclass=_Meta):
    '''
    >>> Charge['e', 'C']
    1.6021765649999947e-19
    '''
    pass


class Dipole(Base, Dimension, metaclass=_Meta):
    '''
    >>> Dipole['yCm', 'D']
    299792.45817809016
    '''
    pass


class Energy(Base, Dimension, metaclass=_Meta):
    '''
    >>> Energy['J', 'cal']
    0.2388458966
    >>> Energy['kcal', 'Btu']
    3.9683205782473134
    '''
    pass


class Force(Base, Dimension, metaclass=_Meta):
    '''
    >>> Force['N', 'lbf']
    0.22480894310000002
    '''
    pass


class Frequency(Base, Dimension, metaclass=_Meta):
    '''
    >>> Frequency['1_s', 'Hz']
    1.0
    '''
    pass


class MolarMass(Base, Dimension, metaclass=_Meta):
    '''
    >>> MolarMass['g_mol', 'kg_mol']
    0.001
    '''
    pass
