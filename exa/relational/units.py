# -*- coding: utf-8 -*-
'''
Units and Dimensions
===============================================
'''
from exa.relational.base import Base, Meta, Column, String, Float
from exa.relational.base import session, commit


class DimensionMeta(Meta):
    '''
    '''
    def _getitem(self, key):
        commit()
        if isinstance(key, tuple):
            return self.get_factor(key)

    def get_factor(self, key):
        commit()
        f = key[0]
        t = key[1]
        return session.query(self).filter(and_(
            self.from_unit == f,
            self.to_unit == t
        )).all()[0].factor


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


class Length(Base, Dimension, metaclass=DimensionMeta):
    pass
class Mass(Base, Dimension, metaclass=DimensionMeta):
    pass
class Time(Base, Dimension, metaclass=DimensionMeta):
    pass
class Current(Base, Dimension, metaclass=DimensionMeta):
    pass
class Temperature(Base, Dimension, metaclass=DimensionMeta):
    pass
class Amount(Base, Dimension, metaclass=DimensionMeta):
    pass
class Luminosity(Base, Dimension, metaclass=DimensionMeta):
    pass
class Dose(Base, Dimension, metaclass=DimensionMeta):
    pass
class Acceleration(Base, Dimension, metaclass=DimensionMeta):
    pass
class Angle(Base, Dimension, metaclass=DimensionMeta):
    pass
class Charge(Base, Dimension, metaclass=DimensionMeta):
    pass
class Dipole(Base, Dimension, metaclass=DimensionMeta):
    pass
class Energy(Base, Dimension, metaclass=DimensionMeta):
    pass
class Force(Base, Dimension, metaclass=DimensionMeta):
    pass
class Frequency(Base, Dimension, metaclass=DimensionMeta):
    pass
class MolarMass(Base, Dimension, metaclass=DimensionMeta):
    pass
