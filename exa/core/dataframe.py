# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
DataFrame
########################
Dataframes are tabular like data objects with columns and indices. They can
represent multi-dimensional, multi-featured data. See `pandas DataFrame`_ for
more information.

In order to build data processing and visualization systems, a known and
systematic data structure is required. The :class:`~exa.core.dataframe.DataFrame`
provides this by enforcing minimum required columns. This allows for processing
and visualization algorithms to be built around dataframes containing known
data (such as coordinates or fields).

The :class:`~exa.core.dataframe.DataFrame` also provides support for additional
metadata using the ``meta`` attribute, similar to other data objects provided
within this framework. In all other aspects, this object behaves identically to
its `pandas DataFrame`_ counterpart.

.. _pandas DataFrame: http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html
"""
import pandas as pd
from .base import Base


class ColumnError(Exception):
    """Raised when a required dimension or feature (column) is missing."""
    @staticmethod
    def default(*columns):
        cols = ", ".join(columns)
        msg = "Missing required column(s): {}"
        return msg.format(cols)

    def __init__(self, *columns, **kwargs):
        msg = kwargs.pop("msg", None)
        msg = self.default(*columns) if msg is None else msg
        super(ColumnError, self).__init__(msg)


class DataFrame(pd.DataFrame, Base):
    """
    A dataframe like object with support for required columns.
    """
    _metadata = ("name", "meta")
    _required_columns = None
    _col_descriptions = None
    _aliases = None

    def info(self):
        """Information about the current object."""
        inf = pd.Series(self.columns).to_frame().set_index(0)
        inf.index.name = "column"
        inf['description'] = ""
        inf['aliases'] = ""
        if self._col_descriptions is not None:
            inf['description'] = inf.index.map(lambda idx: self._col_descriptions[idx] if idx in self._col_descriptions else "")
        if self._aliases is not None:
            inf['aliases'] = inf.index.map(lambda idx: self._aliases[idx] if idx in self._aliases else "")
        return inf

    @property
    def _constructor(self):
        return DataFrame

    def _html_repr_(self):
        return super(DataFrame, self)._html_repr_()

    def __init__(self, *args, **kwargs):
        name = kwargs.pop("name", None)
        meta = kwargs.pop("meta", None)
        super(DataFrame, self).__init__(*args, **kwargs)
        if self._required_columns is not None:
            missing = set(self._required_columns).difference(self.columns)
            if len(missing) > 0:
                raise ColumnError(*missing)
        self.name = name
        self.meta = meta
