# -*- coding: utf-8 -*-
'''
Isotope Data
===============================================
'''
from itertools import product
from sqlalchemy import String, Float
from exa import _pd as pd
from exa.relational.base import Base, Column, Integer
from exa.relational.base import Meta as _Meta
from exa.relational.base import db_sess


class Meta(_Meta):
    '''
    This class provides methods available to the :class:`~exa.relational.isotopes.Isotope`
    class object used to efficiently look up data stored in the database.
    '''
    _symbols_to_radii_map = None    # {'HH': 1.21, ...}
    _element_mass_map = None        # See the properties below: this pattern is
    _Z_to_symbol_map = None         # used so that we cache the result once computed.
    _symbol_to_Z_map = None         # {'H': 1, ...}
    _symbol_to_radius_map = None
    _symbol_to_color_map = None

    @property
    def symbols_to_radii_map(self):
        if self._symbols_to_radii_map is None:
            df = self.table()[['symbol', 'radius']].drop_duplicates('symbol')
            sum_radii = df['radius'].values
            sum_radii = [a + b for a, b in product(sum_radii, sum_radii)]
            symbol_pairs = df['symbol'].values
            symbol_pairs = [''.join(pair) for pair in product(symbol_pairs, symbol_pairs)]
            df = pd.DataFrame.from_dict({'symbols': symbol_pairs, 'radius': sum_radii})
            df.set_index('symbols', inplace=True)
            df.index.names = [None]
            self._symbols_to_radii_map = df['radius']
        return self._symbols_to_radii_map

    @property
    def element_mass_map(self):
        '''
        Dictionary of element keys and element mass values.
        '''
        if self._element_mass_map is None:
            df = self.table()[['symbol', 'mass', 'af']].dropna()
            df['fmass'] = df['mass'] * df['af']
            self._element_mass_map = df.groupby('symbol')['fmass'].sum()
        return self._element_mass_map

    @property
    def Z_to_symbol_map(self):
        '''
        Dictionary of proton number (Z) keys and symbol values.
        '''
        if self._Z_to_symbol_map is None:
            self._Z_to_symbol_map = self.table()[['symbol', 'Z']].set_index('Z')['symbol']
        return self._Z_to_symbol_map

    @property
    def symbol_to_Z_map(self):
        '''
        Dictionary of symbol keys and proton number (Z) values.
        '''
        if self._symbol_to_Z_map is None:
            self._symbol_to_Z_map = self.table()[['symbol', 'Z']].set_index('symbol')['Z']
        return self._symbol_to_Z_map

    @property
    def symbol_to_radius_map(self):
        '''
        Dictionary of symbol keys and covalent radii values.
        '''
        if self._symbol_to_radius_map is None:
            df = self.table()[['symbol', 'radius']].drop_duplicates('symbol').set_index('symbol')['radius']
            self._symbol_to_radius_map = df
        return self._symbol_to_radius_map

    @property
    def symbol_to_color_map(self):
        '''
        Dictionary of symbol keys and isotope color values.
        '''
        if self._symbol_to_color_map is None:
            df = self.table()[['symbol', 'color']].drop_duplicates('symbol').set_index('symbol')['color']
            self._symbol_to_color_map = df
        return self._symbol_to_color_map

    def get_by_strid(self, strid):
        '''
        Get stope by string of format 'ZA' (e.g. '1H').

        Args:
            strid (str): Standard isotope string

        Returns:
            isotope (:class:`~exa.relational.isotopes.Isotope`): Isotope object
        '''
        return db_sess.query(self).filter(self.strid == strid).one()

    def get_by_symbol(self, symbol):
        '''
        Get all isotopes with a given symbol.

        Args:
            symbol (str): Isotope or element 0, 1, or 2 character symbol

        Returns:
            isotopes (list): List of isotope with the given symbol
        '''
        return db_sess.query(self).filter(self.symbol == symbol).all()

    def get_by_szuid(self, szuid):
        '''
        Get isotope with a given Szudzik id.

        Args:
            szuid (int): Szudzik id for a given isotope

        Returns:
            isotope (:class:`~exa.relational.isotopes.Isotope`): Isotope object
        '''
        return db_sess.query(self).filter(self.szuid == szuid).one()

    def get_by_pkid(self, pkid):
        '''
        Get isotope with a given primary key (pkid).

        Args:
            pkid (int): Isotope primary key

        Returns:
            isotope (:class:`~exa.relational.isotopes.Isotope`): Isotope object
        '''
        return db_sess.query(self).filter(self.pkid == pkid).one()

    def __getitem__(self, key):
        '''
        Custom lookup for isotopes: if string with leading digit, get by
        istope string id, else get by symbol. If integer, try first to get by
        Szudzik id, then try to get by primary key id.
        '''
        if isinstance(key, str):
            if key[0].isdigit():
                return self.get_by_strid(key)
            else:
                return self.get_by_symbol(key)
        elif isinstance(key, int):
            try:
                return self.get_by_szuid(key)
            except:
                return self.get_by_pkid(key)
        else:
            raise TypeError('Key type {0} not supported.'.format(type(key)))


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

    @classmethod
    def symbol_to_mass(cls):
        return cls.element_mass_map

    def __repr__(self):
        return '{0}{1}'.format(self.A, self.symbol)
