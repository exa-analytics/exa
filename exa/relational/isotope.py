# -*- coding: utf-8 -*-
'''
Table of Isotopes
###########################################
This module provides an interface for interacting with isotopes of atoms; the
extended periodic table. For convenience, functions are provided for obtaining
traditionally used elements. This module also provides mappers for commonly
used dataframe manipulations.
'''
import numpy as np
import pandas as pd
from itertools import product
from sqlalchemy import String, Float
from sqlalchemy import Column, Integer, String
from exa._config import config
from exa.relational.base import BaseMeta, Base, scoped_session
from exa.iterative import product_sum_2f, product_add_2


# Mappers are series objects that appear in commonly used dataframe manipulations
symbol_to_radius = None
symbol_to_color = None
symbol_to_Z = None
Z_to_symbol = None
symbols_to_radii = None
symbol_to_element_mass = None


class Meta(BaseMeta):
    '''
    This class provides methods available to the :class:`~exa.relational.isotope.Isotope`
    class object used to efficiently look up data stored in the database.
    '''
    def get_by_strid(cls, strid):
        '''
        Get an isotope using a string id.
        '''
        with scoped_session(expire_on_commit=False) as s:
            return s.query(cls).filter(cls.strid == strid).one()

    def get_by_symbol(cls, symbol):
        '''
        Get an isotope using a string id.
        '''
        with scoped_session(expire_on_commit=False) as s:
            return s.query(cls).filter(cls.symbol == symbol).all()

    def get_element(cls, name_or_symbol):
        '''
        Get (i.e. compute) the element with the given name or symbol (an
        element's data is given as an average over isotopic composition).
        '''
        raise NotImplementedError()

    def _getitem(cls, key):
        if isinstance(key, str):
            if key[0].isdigit():
                return cls.get_by_strid(key)
            elif len(key) <= 3:
                return cls.get_by_symbol(key)
            return cls.get_by_name(key)


class Isotope(Base, metaclass=Meta):
    '''
    A variant of a chemical element with a specific proton and neutron count.

    >>> h = Isotope['1H']
    >>> h.A
    1
    >>> h.Z
    1
    >>> h.mass
    1.0078250321
    >>> Isotope['C']
    [8C, 9C, 10C, 11C, 12C, 13C, 14C, 15C, 16C, 17C, 18C, 19C, 20C, 21C, 22C]
    >>> Isotope['13C'].szuid
    175
    >>> c = Isotope[57]
    >>> c.A
    13
    >>> c.Z
    6
    >>> c.strid
    '13C'
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


# Dynamically create a number of commonly used dataframe mappings after
# static data has been loaded
def init_mappers():
    '''
    Initialize commonly used dataframe mappers (in memory).
    '''
    isotopedf = Isotope.to_frame()
    init_symbols_to_radii(isotopedf)
    init_symbol_to_element_mass(isotopedf)
    init_symbol_to_radius(isotopedf)
    init_symbol_to_color(isotopedf)
    init_symbol_to_Z(isotopedf)


def init_symbol_to_Z(isotopedf):
    '''
    Initialize the **symbol_to_Z** mapper.
    '''
    global symbol_to_Z
    global Z_to_symbol
    symbol_to_Z = isotopedf.drop_duplicates('symbol')
    symbol_to_Z = symbol_to_Z.set_index('symbol')['Z']
    Z_to_symbol = isotopedf.drop_duplicates('Z')
    Z_to_symbol = Z_to_symbol.set_index('Z')['symbol']


def init_symbols_to_radii(isotopedf):
    '''
    Initialize the **symbols_to_radii** mapper
    '''
    global symbols_to_radii
    df = isotopedf.drop_duplicates('symbol')
    symbol = df['symbol'].values
    radius = df['radius'].values
    symbols = product_add_2(symbol, symbol)
    radii = product_sum_2f(radius, radius)
    symbols_to_radii = pd.Series(radii)
    symbols_to_radii.index = symbols


def init_symbol_to_element_mass(isotopedf):
    '''
    Initialize the **symbol_to_element_mass** mapper.
    '''
    global symbol_to_element_mass
    isotopedf['fmass'] = isotopedf['mass'] * isotopedf['af']
    topes = isotopedf.groupby('name')
    n = topes.ngroups
    masses = np.empty((n, ), dtype=np.float64)
    symbols = np.empty((n, ), dtype='O')
    for i, (name, element) in enumerate(topes):
        symbols[i] = element['symbol'].values[-1]
        masses[i] = element['fmass'].sum()
    symbol_to_element_mass = pd.Series(masses)
    symbol_to_element_mass.index = symbols


def init_symbol_to_radius(isotopedf):
    '''
    Initialize the **symbol_to_radius** mapper.
    '''
    global symbol_to_radius
    symbol_to_radius = isotopedf.drop_duplicates('symbol')
    symbol_to_radius = symbol_to_radius.set_index('symbol')['radius']


def init_symbol_to_color(isotopedf):
    '''
    Initialize the **symbol_to_color** mapper.
    '''
    global symbol_to_color
    symbol_to_color = isotopedf.drop_duplicates('symbol')
    symbol_to_color = symbol_to_color.set_index('symbol')['color']
