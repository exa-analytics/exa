# -*- coding: utf-8 -*-
'''
Physical Constants
===============================================
'''
from sqlalchemy import String, Float, Column
from exa.relational.base import Base


class Constant(Base):
    '''
    Physical constants and their values in SI units.

    >>> Eh = Constant['Eh']
    >>> Eh.value
    4.35974434e-18
    '''
    symbol = Column(String, nullable=False)
    value = Column(Float, nullable=False)

    def __repr__(self):
        return 'Constant({0}: {1})'.format(self.symbol, self.value)
