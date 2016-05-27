# -*- coding: utf-8 -*-
'''
Physical Constants
===============================================
'''
from sqlalchemy import String, Float, Column
from exa.relational.base import Base, BaseMeta, SessionFactory


class Meta(BaseMeta):
    '''
    Metaclass for :class:`~exa.relational.constant.Constant`.
    '''
    def get_by_symbol(cls, symbol):
        '''
        Get a constant by symbol.
        '''
        s = SessionFactory()
        return s.query(cls).filter(cls.symbol == symbol).one()

    def _getitem(cls, symbol):
        return cls.get_by_symbol(symbol)


class Constant(Base, metaclass=Meta):
    '''
    Physical constants and their values in SI units.

    >>> Eh = Constant['Eh']
    >>> Eh.value
    4.35974434e-18

    To inspect available physical constants use the to_frame method.

    >>> constants = Constant.to_frame()
    '''
    symbol = Column(String, nullable=False)
    value = Column(Float, nullable=False)

    def __repr__(self):
        return 'Constant({0}: {1})'.format(self.symbol, self.value)
