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
    name = Unicode()
    meta = Dict()
    source = Any(allow_none=True)
    source_cfg = Unicode()
    source_args = List()
    source_kws = Dict()
    index = Unicode()
    columns = List()
    cardinal = Tuple()
    categories = Dict()

    # TODO : comb through numerical.py
    #        and find all useful attributes and
    #        secret sauce and expose on Data.
    #
    #        also what to do about Field?
    #        is it a subclass of data?

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
            self.source_args = []
            self.sourcs_kws = {}

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
        src_cfg = cfg.get('source_cfg', None)
        # Assume source is a path to a method_name or ClassName
        # and is fully qualified by an importable module
        if source is not None:
            try:
                *mod, obj = source.split('.')
                mod = importlib.import_module('.'.join(mod))
                if obj.istitle(): # class to instantiate
                    # support loading source from a cfg file
                    if src_cfg:
                        source = getattr(mod, obj).from_yml(src_cfg)
                    # otherwise empty class instantiation?
                    else:
                        source = getattr(mod, obj)()
                else: # assume source is a function
                    source = getattr(mod, obj)
            except Exception as e:
                self.log.error(f"attempt to import source failed: {e}")
                source = None
        return cls(source=source, **cfg)

    def groupby(self):
        pass

    def slice(self):
        pass

    def memory(self):
        pass

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
        if _data is None and self.source is not None:
            _data = self.source(
                *self.source_args, **self.source_kws
            )
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
        return self._set_categories(df)

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
                    "categorical {} specified but not in data".format(col)
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
