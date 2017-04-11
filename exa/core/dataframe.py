# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
DataFrame
########################
"""
import six
import pandas as pd
from .base import ABCBaseMeta, ABCBase
from .dataseries import DataSeries


class DataFrameMeta(ABCBaseMeta):
    dimensions = (list, tuple)
    aliases = dict


class DataFrame(six.with_metaclass(DataFrameMeta, pd.DataFrame, ABCBase)):
    _metadata = ["name", "dimensions", "uid", "meta", "aliases"]
    _constructor_sliced = DataSeries

    @property
    def _constructor(self):
        return DataFrame
