# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Custom Indexers
###################################
Alias supporting indexers

.. _pandas: http://pandas.pydata.org/
"""
import six
import pandas as pd
from pandas.core.indexing import (_IXIndexer, _iLocIndexer, _LocIndexer,
                                  _AtIndexer, _iAtIndexer)


class IXIndexer(_IXIndexer):
    """
    Custom :class:`~pandas.core.indexing._IXIndexer` that checks for column
    aliases.
    """
    def __getitem__(self, key):
        key = self.obj.aliases[key]
        return super(IXIndexer, self).__getitem__(key)


def indexers():
    return [("ix", IXIndexer), ('iloc', _iLocIndexer), ('loc', _LocIndexer),
            ('at', _AtIndexer), ('iat', _iAtIndexer)]
