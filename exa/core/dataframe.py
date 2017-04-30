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
from .base import ABCBase


class ColumnError(Exception):
    """Raised when a required dimension or feature (column) is missing."""
    @staticmethod
    def default(*columns):
        cols = ", ".join(*columns)
        msg = "Missing required column(s): {}"
        return msg.format(cols)

    def __init__(self, *columns, msg=None):
        msg = self.default(*columns) if msg is None else msg
        super(ColumnError, self).__init__(msg)


class DataFrame(pd.DataFrame, ABCBase):
    """
    A dataframe like object with support for required columns.
    """
    _metadata = ("name", "uid", "meta")
    _required_columns = None
    _col_descriptions = None
    _aliases = None

    def info(self):
        """Information about the current object."""
        inf = {'required': self._required_columns, 'aliases': self._aliases,
               'descriptions': self._col_descriptions}
        return inf

    @property
    def _constructor(self):
        return DataFrame

    def __init__(self, *args, **kwargs):
        name = kwargs.pop("name", None)
        uid = kwargs.pop("uid", None)
        meta = kwargs.pop("meta", None)
        super(DataFrame, self).__init__(*args, **kwargs)
        if self._required_columns is not None:
            missing = set(self._required_columns).difference(self.columns)
            if len(missing) > 0:
                raise ColumnError(*missing)
        self.name = name
        self.uid = uid
        self.meta = meta
