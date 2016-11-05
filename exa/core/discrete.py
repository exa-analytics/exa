# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Discrete Data Objects
###################################
Custom discrete data objects (such as series, dataframes, etc.) provide easy
description of relationships. There are three types of relationships, one-to-one
(matching index names), one-to-many (index name in columns), and many-to-many
(matching columns).
"""
import six
import pandas as pd
from exa.core.typed import TypedMeta
from exa.cms.unit import units


class Series(pd.Series):
    """A series is a single valued n dimensional array."""
    _metadata = ['name', 'units']

    def convert_units(self, to_unit):
        """Convert units."""
        from_unit = self.units
        unit = self._dim
        if unit is not None:
            self.values *= unit[from_unit, to_unit]
            self.units = to_unit

    @property
    def _constructor(self):
        return Series

    def _auto_convert_units(self, other):
        if isinstance(other, Series):
            factor = units[(other.units, self.units)]
            return other.values * factor
        return other

    def __add__(self, other, *args, **kwargs):
        if isinstance(other, Series):
            other = self._auto_convert_units(other)
        return super(Series, self).__add__(other, *args, **kwargs).__finalize__(self)

    def __finalize__(self, other, method=None, **kwargs):
        for name in self._metadata:
            object.__setattr__(self, name, getattr(other, name, None))
        return self

    def __init__(self, *args, **kwargs):
        units = kwargs.pop("units", None)
        super(Series, self).__init__(*args, **kwargs)
        self.units = units


#class DataFrame(pd.DataFrame):
#    """
#    """
#    def __init__(self, *args, **kwargs):
#        super(DataFrame, self).__init__(*args, **kwargs)
#        if self.index.name is None:
#            self.index.name = self.name
#
#
#class Frame(DataFrame):
#    """
#    """
#    pass
#
#
#class Atom(DataFrame):
#    """
#    """
#    pass
#
#
#class UnitAtom(DataFrame):
#    """
#    """
#    _index_name = "atom"
#
#class AtomTwo(DataFrame):
#    """
#    """
#    pass
#
#class Molecule(DataFrame):
#    """"""
#    _relations = [""]
#
#


#def network(dataobjs):
#    obj0list = []
#    obj1list = []
#    rellist = []
#    for name0, obj0 in dataobjs:
#        for name1, obj1 in dataobjs:
#            if obj0 is obj1:
#                continue
#            obj0list.append(name0)
#            obj1list.append(name1)
#            if obj0.index.name == obj1.index.name:
#                rellist.append("index-index")
#            elif check_one_to_many(obj0, obj1):
#            elif (obj0.index.name in obj1.columns or obj1.index.name in obj0.columns):
#                rellist.append("index-column")
#            elif any([col in obj1.columns for col in obj0.columns]) or any([col in obj0.columns for col in obj1.columns]):
#                rellist.append("column-column")
#            else:
#                rellist.append(None)
#    return pd.DataFrame.from_dict({"obj0": obj0list, "obj1": obj1list, "direct": rellist})
#
#
#def check_one_to_one(obj0, obj1):
#    """
#    Check if a one-to-one relationship exists between two data objects.
#
#    Args:
#        obj0: Data object (series, dataframe, etc.)
#        obj1: Other data object
#
#    Returns:
#        rel (bool): True if one-to-one relationship exists
#    """
#    if obj0.index.name == obj1.index.name:
#        return True
#    return False
#
#
#def check_one_to_many(obj0, obj1):
#    """
#    Check if a one-to-many relationship exists between two data objects.
#
#    Args:
#        obj0: Data object (series, dataframe, etc.)
#        obj1: Other data object
#
#    Returns:
#        rel (bool): True if one-to-many relationship exists
#    """
#    obj0_name = obj0.index.name + "_"
#    obj1_name = obj1.index.name + "_"
#
