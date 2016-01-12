# -*- coding: utf-8 -*-
'''
Isotope Data
===============================================
'''
from exa.relational.base import Base, Column, String, Integer, Float
from exa.relational.base import Meta as _Meta
from exa.relational.base import session, commit

class Meta(_Meta):
    '''
    '''
    def get_by_symbol(self, symbol):
        '''
        '''
        return session.query(self).filter(self.symbol == symbol).all()

    def get_by_strid(self, element):
        '''
        '''
        return session.query(self).filter(self.strid == element).all()[0]

    def get_szuid(self, number):
        '''
        '''
        return session.query(self).filter(self.szuid == number).all()[0]

    def get_element(self, key, by='symbol'):
        '''
        Args:
            by (str): One of 'symbol' or 'znum' or 'asym'
            key: Symbol or proton number (znum) or 'ASymbol' (1H, 12C, etc)
        '''
        if by == 'symbol':
            return session.query(self).filter(self.symbol == key).order_by(self.af).all()[-1]
        elif by == 'znum':
            return session.query(self).filter(self.Z == key).order_by(self.af).all()[-1]
        elif by == 'asym':
            return session.query(self).filter(self.strid == key).all()[-1]
        else:
            raise NotImplementedError()

    def get_elements(self, keys, by='symbol'):
        '''
        '''
        return [self.get_element(key, by=by) for key in keys]

    def _getitem(self, key):
        if isinstance(key, str):
            if key[0].isdigit():
                return self.get_by_strid(key)
            else:
                return self.get_by_symbol(key)
        elif isinstance(key, int):
            return self.get_by_szuid(key)
        else:
            raise TypeError('Key type {0} not supported.'.format(type(key)))

    def __getitem__(self, key):
        commit()
        return self._getitem(key)


class Isotope(Base, metaclass=Meta):
    '''
    A variant of a chemical element with a specific proton and neutron count.
    '''
    A = Column(Integer, nullable=False)
    Z = Column(Integer, nullable=False)
    af = Column(Float)
    eaf = Column(Float)
    color = Column(Integer)
    radius = Column(Float)
    gfactor = Column(Float)
    mass = Column(Float)
    emass = Column(Float)
    name = Column(String(length=16))
    eneg = Column(Float)
    quadmom = Column(Float)
    spin = Column(Float)
    symbol = Column(String(length=3))
    szuid = Column(Integer)
    strid = Column(Integer)

    def __repr__(self):
        return '{0}{1}'.format(self.A, self.symbol)
