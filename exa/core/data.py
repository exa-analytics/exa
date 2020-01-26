# -*- coding: utf-8 -*-
# Copyright (c) 2015-2019, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Data
########
"""
from traitlets import Unicode, Instance, Integer, Float, Any
from traitlets import validate, default, observe
from traitlets import TraitError
from traitlets.config import Configurable
import pandas as pd

import exa

class Data(exa.Base, Configurable):
    """An interface to separate data provider routing
    logic and simplify managing multiple data concepts
    in the container.
    """
    myvar = Integer(5).tag(config=True)
    name = Unicode()
    source = Any(allow_none=True)
    # TODO : port the concept of _index,
    #        _categories, _columns to
    #        traits and set up validators
    #        to get back strong-typing behavior
    #        inside of the dataframe
    # this likely involves making _data a
    # first class trait so we can observe
    # when it is updated.

    @validate('source')
    def _validate_source(self, prop):
        """source must implement __call__"""
        if not callable(prop['value']):
            raise TraitError("source must be callable")
        return prop['value']

    @observe('source')
    def _observe_source(self, prop):
        """Invalidate the stored data if source changes"""
        self._data = None

    @validate('name')
    def _validate_name(self, prop):
        return prop['value'].lower()

    @default('name')
    def _default_name(self):
        return self.__class__.__name__

    def data(self, df=None):
        """Return the currently stored data in the
        Data object. If df is provided, store that
        as the current data and return it. Otherwise,
        determine the provider to execute to obtain
        the data, store it and return it.
        """
        # if provided, store df in Data and return it
        if df is not None:
            self._data = df
        # otherwise, lazily evaluate source provider
        elif self._data is None:
            if self.source is not None:
                # TODO: reintroduce the automated getattr(attr, getter_attr())
                #       with _getter_prefix behavior on a
                #       base class somewhere that providers
                #       inherit from
                # Alternatively; implement a __call__ method
                #       on sources which manages that on a per
                #       provider basis. The way the validate is
                #       set right now forces the latter approach
                # To support arbitrary callables we should add support
                #       for source's *args and **kws
                self._data = self.source()
        # return the now cached data
        return self._data

    def __init__(self, *args, df=None, **kws):
        self._data = df
        super().__init__(*args, **kws)



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
    """Following suite until more is decided on
    Editor updates.
    """
    path = exa.cfg.resource('constants.json')
    df = pd.read_json(path, orient='values')
    return df


class Constants(Data):

    def __init__(self, *args, **kws):
        source = kws.pop('source', load_constants)
        super().__init__(*args, source=source, **kws)

