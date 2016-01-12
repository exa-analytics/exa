# -*- coding: utf-8 -*-
'''
Units and Dimensions
===============================================
'''
from exa.relational.base import Base, Column, String, Float
from exa.relational.base import session, commit


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


class Length(Base, Dimension):
    pass
class Mass(Base, Dimension):
    pass
class Time(Base, Dimension):
    pass
class Current(Base, Dimension):
    pass
class Temperature(Base, Dimension):
    pass
class Amount(Base, Dimension):
    pass
class Luminosity(Base, Dimension):
    pass
class Dose(Base, Dimension):
    pass
class Acceleration(Base, Dimension):
    pass
class Angle(Base, Dimension):
    pass
class Charge(Base, Dimension):
    pass
class Dipole(Base, Dimension):
    pass
class Energy(Base, Dimension):
    pass
class Force(Base, Dimension):
    pass
class Frequency(Base, Dimension):
    pass
class MolarMass(Base, Dimension):
    pass
