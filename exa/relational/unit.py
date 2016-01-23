# -*- coding: utf-8 -*-
'''
Units and Dimensions
===============================================
'''
from sqlalchemy import and_, String, Float
from exa.relational.base import Meta as _Meta
from exa.relational.base import Base, Column, db_sess, commit
from exa.relational.errors import FactorNotFound


class Meta(_Meta):
    '''
    '''
    def _getitem(cls, key):
        if isinstance(key, tuple):
            return cls.get_factor(key)
        else:
            raise TypeError('Key must be a tuple not {0}'.format(type(key)))

    def get_factor(cls, key):
        f = key[0]
        t = key[1]
        factor = db_sess.query(cls).filter(and_(cls.from_unit == f, cls.to_unit == t)).all()
        if len(factor) == 1:
            return factor[0].factor
        else:
            raise FactorNotFound(f, t)

    def __getitem__(cls, key):
        commit()
        return cls._getitem(key)

    def from_alias(cls, source, target):
        '''
        Look up a source unit by alias.
        '''
        f = cls.aliases[source.lower()]
        return cls[f, target]


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
