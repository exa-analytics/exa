# -*- coding: utf-8 -*-
'''
Units and Dimensions
===============================================
This module provides relational classes for unit conversion tables.
'''
from sqlalchemy import and_, String, Float, Column
from exa.relational.base import BaseMeta, Base, SessionMaker


class Meta(BaseMeta):
    '''
    '''
    aliases = {}

    def _getitem(cls, key):
        '''
        Allows for selection of a conversion factor using the following syntax:

        .. code-block:: Python

            from exa.relational import Length
            Length['angstrom', 'au']
            1.88973
            Length['A', 'au']
            1.88973
        '''
        if isinstance(key, tuple):
            f = cls.aliases[key[0]] if key[0] in cls.aliases else key[0]
            t = cls.aliases[key[1]] if key[1] in cls.aliases else key[1]
            session = SessionMaker()
            factor = session.query(cls).filter(and_(cls.from_unit==f, cls.to_unit==t)).one().factor
            session.close()
            return factor
        else:
            raise TypeError('Usage requires syntax Class["from_unit", "to_unit"]')


class Dimension:
    '''
    Generic class for physical dimension conversions. Doesn't do anything
    by itself but is inherited by specific dimension classes.

    Attributes
        from_unit (str): Unit to convert from
        to_unit (str): Unit to convert to
        factor (float): Conversion factor

    Methods
        units: Displays a list of possible units

    See Also
        :class:`~exa.relational.Length`
    '''
    from_unit = Column(String(8), nullable=False)
    to_unit = Column(String(8), nullable=False)
    factor = Column(Float, nullable=False)


class Length(Base, Dimension, metaclass=Meta):
    '''
    Length conversions.
    '''
    aliases = {
        'bohr': 'au',
        'angstrom': 'A',
        u'\u212B': 'A',
        u'\u212Bngstrom': 'A',
        'a0': 'au'
    }


class Mass(Base, Dimension, metaclass=Meta):
    pass
class Time(Base, Dimension, metaclass=Meta):
    pass
class Current(Base, Dimension, metaclass=Meta):
    pass
class Temperature(Base, Dimension, metaclass=Meta):
    pass
class Amount(Base, Dimension, metaclass=Meta):
    pass
class Luminosity(Base, Dimension, metaclass=Meta):
    pass
class Dose(Base, Dimension, metaclass=Meta):
    pass
class Acceleration(Base, Dimension, metaclass=Meta):
    pass
class Angle(Base, Dimension, metaclass=Meta):
    pass
class Charge(Base, Dimension, metaclass=Meta):
    pass
class Dipole(Base, Dimension, metaclass=Meta):
    pass
class Energy(Base, Dimension, metaclass=Meta):
    pass
class Force(Base, Dimension, metaclass=Meta):
    pass
class Frequency(Base, Dimension, metaclass=Meta):
    pass
class MolarMass(Base, Dimension, metaclass=Meta):
    pass
