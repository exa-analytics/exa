# -*- coding: utf-8 -*-
'''
Isotope Data
===============================================
'''
from itertools import product
from sqlalchemy import String, Float
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

    @property
    def symbols_to_radii_map(self):
        '''
        Dictionary of symbol pair keys and sum of radii values.
        '''
        if self._symbols_to_radii_map is None:
            df = self._df()[['symbol', 'radius']].drop_duplicates('symbol')
            sum_radii = df['radius'].values
            sum_radii = [a + b for a, b in product(sum_radii, sum_radii)]
            symbol_pairs = df['symbol'].values
            symbol_pairs = [''.join(pair) for pair in product(symbol_pairs, symbol_pairs)]
            self._symbols_to_radii_map = dict([(symbol_pairs[i], radii) for i, radii in enumerate(sum_radii)])
        return self._symbols_to_radii_map

    @property
    def element_mass_map(self):
        '''
        Dictionary of element keys and element mass values.
        '''
        if self._element_mass_map is None:
            df = self._df()[['symbol', 'mass', 'af']].dropna()
            df['fmass'] = df['mass'] * df['af']
            self._element_mass_map = df.groupby('symbol')['fmass'].sum().to_dict()
        return self._element_mass_map

    @property
    def Z_to_symbol_map(self):
        '''
        Dictionary of proton number (Z) keys and symbol values.
        '''
        if self._Z_to_symbol_map is None:
            if self._symbol_to_Z_map is None:
                self._Z_to_symbol_map = self._df()[['symbol', 'Z']].set_index('Z')['symbol'].to_dict()
            else:
                self._Z_to_symbol_map = {v: k for k, v in self._symbol_to_Z_map.items()}
        return self._Z_to_symbol_map

    @property
    def symbol_to_Z_map(self):
        '''
        Dictionary of symbol keys and proton number (Z) values
        '''
        if self._symbol_to_Z_map is None:
            if self._Z_to_symbol_map is None:
                self._symbol_to_Z_map = self._df()[['symbol', 'Z']].set_index('symbol')['Z'].to_dict()
            else:
                self._symbol_to_Z_map = {v: k for k, v in self._Z_to_symbol_map.items()}
        return self._symbol_to_Z_map

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
    def lookup_sum_radii_by_symbols(cls, symbols):
        '''
        Given a pair of symbols look up the sum of their covalent radii.

        Args:
            symbols (str): Symbol pair (e.g. 'OH')

        Returns:
            r (float): Sum of covalent radii

        See Also:
            :attribute:`~exa.relational.isotopes.Meta.symbols_to_radii_map`
        '''
        return cls.symbols_to_radii_map[symbols]

    @classmethod
    def lookup_mass_by_element(cls, element):
        '''
        Get the element's mass (abundance fraction times isotope mass).

        Args:
            element (str): Element symbol

        Returns:
            mass (float): Element's mass in atomic units (au).
        '''
        return cls.element_mass_map[element]

    @classmethod
    def lookup_symbol_by_Z(cls, Z):
        '''
        Get the element's symbol by the element's proton number (Z).
        '''
        return cls.Z_to_symbol_map[Z]

    @classmethod
    def lookup_Z_by_symbol(cls, symbol):
        '''
        Get the element's proton number (Z) by the element's symbol.
        '''
        return cls.symbol_to_Z_map[symbol]

    def __repr__(self):
        return '{0}{1}'.format(self.A, self.symbol)
