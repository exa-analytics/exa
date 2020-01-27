# Copyright (c) 2015-2020, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Data
########
"""
import importlib

from traitlets import List, Unicode, Dict, Any
from traitlets import validate, default, observe
from traitlets import TraitError
from traitlets.config import Configurable
import pandas as pd
import yaml

import exa
from exa.core.error import RequiredColumnError


# TODO: reintroduce the automated getattr(attr, getter_attr())
#       with _getter_prefix behavior on a
#       base class somewhere that providers
#       inherit from


class Data(exa.Base, Configurable):
    """An interface to separate data provider routing
    logic and simplify managing multiple data concepts
    in the container.
    """
    name = Unicode()
    source = Any(allow_none=True)
    source_args = List()
    source_kws = Dict()
    index = Unicode()
    columns = List()
    categories = Dict()

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
        with open(path, 'r') as f:
            cfg = yaml.safe_load(f.read())
        ver = cfg.pop('version', None)
        if ver != 1:
            raise Exception("version {} not supported".format(ver))
        source = cfg.pop('source', None)
        # Assume source is a path to a method_name or ClassName
        # and is fully qualified by an importable module
        if source is not None:
            try:
                *mod, obj = source.split('.')
                mod = importlib.import_module('.'.join(mod))
                # TODO : do we also support providing init
                #        args and kwargs in case source is class?
                if obj.istitle(): # class to instantiate
                    source = getattr(mod, obj)()
                else: # assume this is a function
                    source = getattr(mod, obj)
            except Exception as e:
                print("attempt to import source failed")
                source = None
        return cls(source=source, **cfg)

    def data(self, df=None, cache=True):
        """Return the currently stored data in the
        Data object. If df is provided, store that
        as the current data and return it. Otherwise,
        determine the provider to execute to obtain
        the data, store it and return it.

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
        # set index name, support set index?
        # or a (multi-col) uniqueness constraint?
        if self.index and df.index.name != self.index:
            self.log.debug("setting index name {}".format(self.index))
            df.index.name = self.index
        # guarantee existence
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
            if col in df.columns:
                conv = {True: typ, False: 'category'}[reverse]
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
    return df.sort_values(by=['symbol', 'A']).reset_index(drop=True)

class Isotopes(Data):
    """An isotopes database data object.

    .. code-block:: python

        import exa
        df = exa.Isotopes().data()
    """

    def __init__(self, *args, **kws):
        source = kws.pop('source', load_isotopes)
        super().__init__(*args, source=source, **kws)


def load_constants():
    """Following suit until more is decided on
    Editor updates.
    """
    path = exa.cfg.resource('constants.json')
    df = pd.read_json(path, orient='values')
    return df


class Constants(Data):

    def __init__(self, *args, **kws):
        source = kws.pop('source', load_constants)
        super().__init__(*args, source=source, **kws)

