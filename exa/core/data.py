# Copyright (c) 2015-2020, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Data
########
"""
import importlib

from traitlets import List, Unicode, Dict, Any, Tuple
from traitlets import validate, default, observe
from traitlets import TraitError
import pandas as pd

import exa
from exa.core.error import RequiredColumnError


class Data(exa.Base):
    """An interface to separate data provider routing
    logic and simplify managing multiple data concepts
    in the container.
    """
    name = Unicode(help="string name of data")
    meta = Dict(help="metadata dictionary")
    source = Any(allow_none=True, help="a callable that takes priority over a __call__ method")
    call_args = List(help="args to pass to call or source")
    call_kws = Dict(help="kwargs to pass to call or source")
    index = Unicode(help="index name") # is this required for Container.network?
    indexes = List(help="columns that guarantee uniqueness")
    columns = List(help="columns that must be present in the dataset")
    # cardinal can maybe just be indexes (or indexes[0]?)
    cardinal = Tuple()
    # generalize to dtypes?
    categories = Dict()

    def slice(self, key):
        """Provide a programmatic way to slice contained
        data without operating on the dataframe directly.
        """

    def groupby(self, columns=None):
        """Convenience method for pandas groupby"""
        cols = columns or self.indexes
        if cols:
            return self.data().groupby(cols)
        self.log.warning("nothing to group by")

    def memory(self):
        """Return the memory footprint of the underlying
        data stored in Data"""
        mem = 0
        df = self.data()
        if isinstance(df, pd.DataFrame):
            mem = df.memory_usage()
        return mem

    def __call__(self, *args, **kws):
        self.log.warning("call not implemented")
        pass

    @validate('source')
    def _validate_source(self, prop):
        """source must implement __call__"""
        if not callable(prop['value']):
            raise TraitError("source must be callable")
        return prop['value']

    @observe('source')
    def _observe_source(self, change):
        """Update stored data if source changes. Nullify
        related traits when source is nullified to reset
        state of the Data object."""
        if change.new is None:
            self._data = None
            self.call_args = []
            self.call_kws = {}

    @validate('name')
    def _validate_name(self, prop):
        return prop['value'].lower()

    @default('name')
    def _default_name(self):
        return self.__class__.__name__

    @classmethod
    def from_yml(cls, path):
        """Load a Data object from a configuration
        file. The intent is not to store the actual
        data in the config, rather all the required
        metadata to source and validate the data for
        itself. Also checks for a configuration file
        specified for the Data's indended source.
        """
        # API loading can probably be generalized
        # and moved to a base class staticmethod.
        cfg = cls._from_yml(path)
        source = cfg.pop('source', None)
        # Assume source is a path to a method_name
        if source is not None:
            try:
                *mod, obj = source.split('.')
                mod = importlib.import_module('.'.join(mod))
                source = getattr(mod, obj)
            except Exception as e:
                source = None
        return cls(source=source, **cfg)

    def data(self, df=None, cache=True):
        """Return the currently stored data in the
        Data object. If df is provided, store that
        as the current data and return it. Otherwise,
        determine the provider to execute to obtain
        the data, store it and return it.

        Note:
            behaves like a setter if df is provided

        Note:
            force re-evaluation of source if cache is False
        """
        _data = getattr(self, '_data', None)
        if not cache:
            _data = None
        if df is not None:
            _data = df
        if _data is None:
            f = self.source or self.__call__
            _data = f(*self.call_args, **self.call_kws)
        self._data = self._validate_data(_data)
        return self._data

    def _validate_data(self, df):
        if not isinstance(df, pd.DataFrame):
            self.log.warning("data not a dataframe, skipping validation")
            return df
        if self.index and df.index.name != self.index:
            self.log.debug("setting index name {}".format(self.index))
            df.index.name = self.index
        missing = set(self.columns).difference(df.columns)
        if missing:
            raise RequiredColumnError(missing, self.name)
        df = self._set_categories(df)
        if self.indexes and df.duplicated(subset=self.indexes).any():
            raise TraitError(f"duplicates in {self.indexes}")
        return df

    def _set_categories(self, df, reverse=False):
        """For specified categorical fields,
        convert to pd.Categoricals.

        Note:
            If reverse is True, revert categories
        """
        for col, typ in self.categories.items():
            conv = {True: typ, False: 'category'}[reverse]
            if col in df.columns:
                df[col] = df[col].astype(conv)
            else:
                self.log.debug(
                    f"categorical {col} specified but not in data"
                )
        return df


def load_isotopes():
    """Minimal working example of a pluggable
    callable to serve as a data provider in the
    Data API.
    """
    path = exa.cfg.resource('isotopes.json')
    df = pd.read_json(path, orient='values')
    df.columns = ('A', 'Z', 'af', 'afu',
                  'cov_radius', 'van_radius', 'g',
                  'mass', 'massu', 'name', 'eneg',
                  'quad', 'spin', 'symbol', 'color')
    # this sorting is to facilitate comparison
    # with the original implementation.
    return df.sort_values(by=['symbol', 'A']).reset_index(drop=True)

def load_constants():
    """Following suit until more is decided on
    Editor updates.
    """
    path = exa.cfg.resource('constants.json')
    return pd.read_json(path, orient='values')

def load_units():
    """Same. Move these loaders somewhere else."""
    path = exa.cfg.resource('units.json')
    return pd.read_json(path, orient='values')

Isotopes = Data(source=load_isotopes, name='isotopes')
Constants = Data(source=load_constants, name='constants')
Units = Data(source=load_units, name='units')


class Field(Data):
    field_values = List()
