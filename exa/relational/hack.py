#-*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Unit Conversions
#########################
This module provides relational classes for unit conversion tables.
"""
import json

with open('/projects/academic/jochena/shared/tjduigna/github/exa/exa/_static/units.json', 'r') as f:
    b = json.load(f)

class Unit(dict):
    """Hack to keep the API of relational in HPC environments."""

    _getitem = dict.__getitem__


class Energy(Unit):
    def __getitem__(self, keys):
        return self._getitem(keys[1]) / self._getitem(keys[0])

Energy = Energy(b['energy'])

class Length(Unit):
    def __getitem__(self, keys):
        return self._getitem(keys[0]) / self._getitem(keys[1])

Length = Length(b['length'])
