# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Unit Conversions
########################################
"""
import six
import pandas as pd


class Unit(object):
    def __setitem__(self, key, value):
        self._values[key] = value

    def __getitem__(self, key):
        if isinstance(key, six.string_types):
            return self._values[key]
        elif isinstance(key, (list, tuple)):
            return self._values[key[1]]/self._values[key[0]]

    def __init__(self, values, name):
        self._values = pd.Series(values)
        self._name = name
