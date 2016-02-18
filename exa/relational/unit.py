# -*- coding: utf-8 -*-
'''
Units and Dimensions
===============================================
'''
from sqlalchemy import and_, String, Float
from exa.relational.base import Meta as _Meta
from exa.relational.base import Base, Column, db_sess


class Meta(_Meta):
    '''
    '''
    def _getitem(cls, key):
        if isinstance(key, tuple):
            f = key[0]
            t = key[1]
            return db_sess.query(cls).filter(and_(cls.from_unit == f, cls.to_unit == t)).one().factor
        else:
            raise TypeError('Key must be a tuple not {0}'.format(type(key)))

    def from_alias(cls, source, target):
        '''
        Attempt to find a conversion factor using alternative names.
        '''
        f = source
        t = target
        try:
            f = cls.aliases[source]
        except:
            try:
                f = cls.aliases[source.lower()]
            except:
                pass
            pass
        try:
            t = cls.aliases[target]
        except:
            try:
                t = cls.aliases[target.lower()]
            except:
                pass
            pass
        return cls[f, t]


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
