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


class Base(object):
    """Base class for discrete data objects."""
    @property
    def _prefix(self):
        return self.__class__.__name__.lower()


class Series(pd.Series, Base):
    """
    A series is an indexed array. The index can be n-dimensional but most often
    is 1-dimensional.
    """
    def copy(self, *args, **kwargs):
        pass
    @property
    def _constructor(self):
        return Series

    def __finalize__(self, *args, **kwargs):
        return self.__class__(self, *args, **kwargs)

    def __init__(self, *args, **kwargs):
        super(Series, self).__init__(*args, **kwargs)
        if self.index.name is None:
            self.index.name = self.name


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
