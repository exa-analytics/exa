# -*- coding: utf-8 -*-
'''
Isotope Data
===============================================
'''
import pandas as pd
from itertools import product
from sqlalchemy import String, Float
from sqlalchemy import Column, Integer, String
from exa.relational.base import BaseMeta, Base, SessionFactory


class _Meta(BaseMeta):
    '''
    This class provides methods available to the :class:`~exa.relational.isotope.Isotope`
    class object used to efficiently look up data stored in the database.
    '''
    _symbols_to_radii_map = None    # {'HH': 1.21, ...}
    _element_mass_map = None        # See the properties below: this pattern is
    _Z_to_symbol_map = None         # used so that we cache the result once computed.
    _symbol_to_Z_map = None         # {'H': 1, ...}
    _symbol_to_radius_map = None
    _symbol_to_color_map = None
    _symbols_to_Z_map = None

    @property
    def symbols_to_Z_map(self):
        '''
        Generate (and store in memory) a quick mapping between symbol pairs
        (e.g OH) and multiplied Z values (8*1=8).
        '''
        if self._symbols_to_Z_map is None:
            df = atomic.Isotope.table()[['symbol', 'Z']].drop_duplicates('symbol').dropna()
            s = df['symbol'].values
            z = df['Z'].values
            sym_pairs = pd.Series([''.join(pair) for pair in product(s, s)])
            Z_product = pd.Series([a*b for a, b in product(z, z)])
            df = pd.DataFrame.from_dict({'symbols': sym_pairs, 'Z_product': Z_product}).set_index('symbols')['Z_product'].astype(np.int64)
            self._symbols_to_Z_map = df
        return self._symbols_to_Z_map

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
            mapper = self.table()[['symbol', 'Z']].drop_duplicates('Z', keep='first').set_index('Z')['symbol']
            self._Z_to_symbol_map = mapper
        return self._Z_to_symbol_map

    @property
    def symbol_to_Z_map(self):
        '''
        Dictionary of symbol keys and proton number (Z) values.
        '''
        if self._symbol_to_Z_map is None:
            self._symbol_to_Z_map = self.table()[['symbol', 'Z']].drop_duplicates().set_index('symbol')['Z']
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
        return SessionFactory().query(self).filter(self.strid == strid).one()

    def get_by_symbol(self, symbol):
        '''
        Get all isotopes with a given symbol.

        Args:
            symbol (str): Isotope or element 0, 1, or 2 character symbol

        Returns:
            isotopes (list): List of isotope with the given symbol
        '''
        return SessionFactory().query(self).filter(self.symbol == symbol).all()

    def get_by_szuid(self, szuid):
        '''
        Get isotope with a given Szudzik id.

        Args:
            szuid (int): Szudzik id for a given isotope

        Returns:
            isotope (:class:`~exa.relational.isotopes.Isotope`): Isotope object
        '''
        return SessionFactory().query(self).filter(self.szuid == szuid).one()

    def get_by_pkid(self, pkid):
        '''
        Get isotope with a given primary key (pkid).

        Args:
            pkid (int): Isotope primary key

        Returns:
            isotope (:class:`~exa.relational.isotopes.Isotope`): Isotope object
        '''
        return SessionFactory().query(self).filter(self.pkid == pkid).one()

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


class Isotope(Base, metaclass=_Meta):
    '''
    A variant of a chemical element with a specific proton and neutron count.

    >>> h = Isotope['1H']
    >>> h.A
    1
    >>> h.Z
    1
    >>> h.mass
    1.0078250321
    >>> Isotope.symbol_to_mass()['H']
    1.0076788974703454
    >>> Isotope['C']
    [8C, 9C, 10C, 11C, 12C, 13C, 14C, 15C, 16C, 17C, 18C, 19C, 20C, 21C, 22C]
    >>> Isotope['13C'].szuid
    175
    >>> c = Isotope[175]
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

    @classmethod
    def symbol_to_mass(cls):
        '''
        Series containing element symbols and their respective mass (in a.u.).

        >>> Isotope.symbol_to_mass().head()    # .head() used to truncate the full series
        symbol
        Ac    227.027752
        Ag    107.869877
        Al     26.981539
        Am    240.630767
        Ar     39.947843
        Name: fmass, dtype: float64

        Note:
            The resulting mass the isotope abundance fraction averaged "element"
            mass.
        '''
        return cls.element_mass_map

    @classmethod
    def symbol_to_radius(cls):
        '''
        Series containing the element symbol and its respective covalent radius.

        >>> Isotope.symbol_to_radius().head()
        symbol
        Dga    0.300000
        H      0.604712
        D      0.604712
        T      0.604712
        He     0.869274
        Name: radius, dtype: float64

        Note:
            The covalent radii data are taken from `this reference`_.

            .. _this reference: http://doi.org/10.1039/b801115j
        '''
        return cls.symbol_to_radius_map

    @classmethod
    def symbols_to_radii(cls):
        '''
        Series containing element symbol pairs and their respective sum of
        covalent radii (in a.u.).

        >>> Isotope.symbols_to_radii().head()    # Try without .head()
        DgaDga    0.600000
        DgaH      0.904712
        DgaD      0.904712
        DgaT      0.904712
        DgaHe     1.169274
        Name: radius, dtype: float64
        '''
        return cls.symbols_to_radii_map

    @classmethod
    def symbol_to_color(cls):
        '''
        Series containing the element symbol and its color

        >>> Isotope.symbol_to_color().head()
        symbol
        Dga    16711935
        H      10197915
        D       5263440
        T       4210752
        He     14286847
        Name: color, dtype: int64
        '''
        return cls.symbol_to_color_map

    @classmethod
    def Z_to_symbol(cls):
        '''
        Series containing Z number (proton number) and the corresponding symbol.

        >>> Isotope.Z_to_symbol().head()
        Z
        0    Dga
        1      H
        2     He
        3     Li
        4     Be
        Name: symbol, dtype: object
        '''
        return cls.Z_to_symbol_map

    @classmethod
    def symbol_to_Z(cls):
        return cls.symbol_to_Z_map

    @classmethod
    def symbols_to_Z(cls):
        return cls.symbols_to_Z_map

    def __repr__(self):
        return '{0}{1}'.format(self.A, self.symbol)
