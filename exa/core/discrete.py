# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Discrete Data Objects
###################################
Exa's data objects (such as series and dataframes) provide all of the power of
`pandas`_ but also a system for describing relationships between data in a
manner easily identifiable by the :class:`~exa.core.container.Container`.

.. _pandas: http://pandas.pydata.org/
"""
import six
import pandas as pd
from pandas.core.ops import _op_descriptions
from exa.cms import unit


class DiscreteMeta(type):
    """
    This class modifies basic operation methods of pandas objects to support
    automatic unit conversion and metadata propagation.
    """
    @staticmethod
    def modify_op(dunder_op):
        """
        """
        def wrapper(self, other, *args, **kwargs):
            #other = self._auto_convert_units(other)
            # Note that in the call to __finalize__ below, self is the argument
            # "other" to __finalize__.
            return getattr(super(Series, self), dunder_op)(other, *args, **kwargs).__finalize__(self)
        return wrapper

    def _auto_convert_units(self, other):
        """Automatically convert units prior to performing a basic operation."""
        if isinstance(other, Series):
            factor = unit.units[(other.units, self.units)]
            return other.values * factor
        return other

    def __finalize__(self, other, method=None, **kwargs):
        """Propagate (for example) metadata."""
        for name in self._metadata:
            object.__setattr__(self, name, getattr(other, name, None))
        return self

    def __new__(mcs, name, bases, clsdict):
        """
        """
        for op, info in _op_descriptions.items():
            op_name = "__{}__".format(op)
            clsdict[op_name] = mcs.modify_op(op_name)
            if info['reverse'] is not None:
                op_name = "__{}__".format(info['reverse'])
                clsdict[op_name] = mcs.modify_op(op_name)
        clsdict['_auto_convert_units'] = mcs._auto_convert_units
        clsdict['__finalize__'] = mcs.__finalize__
        return super(DiscreteMeta, mcs).__new__(mcs, name, bases, clsdict)


class Series(six.with_metaclass(DiscreteMeta, pd.Series)):
    """
    A series is a single valued n dimensional array.

    Single valued means that a series only carries a single type or column of
    data (of a specific kind). Each element of the array is labeled by an index.
    The index can be a single dimension (e.g. an array of integers) or
    multidimensional. The dimensions of a series are determined by its index.
    """
    _metadata = ['name', 'units']

    def convert_units(self, to_unit):
        """
        Convert units (inplace) of the current series.

        .. code-block: Python

            energies = Series([1, 2, 3], units="kJ")
            print(energies.units)      # kJ
            energies.convert_units("J")
            print(energies)            # 1000, 2000, 3000
            print(energies.units)      # J

        Args:
            to_unit (str): Unit to convert to
        """
        if self.units is not None:
            self *= unit.units[(self.units, to_unit)]
            self.units = to_unit

    @property
    def _constructor(self):
        return Series

    def __init__(self, *args, **kwargs):
        units = kwargs.pop("units", None)
        super(Series, self).__init__(*args, **kwargs)
        self.units = units


class DataFrame(six.with_metaclass(DiscreteMeta, pd.DataFrame)):
    pass

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
