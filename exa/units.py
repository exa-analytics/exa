# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Units
############################
"""
import sys as _sys
from pkg_resources import resource_filename as _resource_filename
from .special import Singleton as _Singleton
from .core.editor import Editor as _Editor


class _Unit(_Singleton):
    """A metaclass for creating units."""
    def __new__(mcs, name, bases, clsdict):
        mcs.__repr__ = lambda self: "{}({}, {})".format(self.__class__.__name__, self._name, repr(self._value))
        return super(_Unit, mcs).__new__(mcs, name, bases, clsdict)


def _create():
    """Generate the isotopes and elements API from their static data."""
    dct = _Editor(_path).to_data('json')
    for lclsname, unitvalues in dct.items():
        clsname = lclsname.title()
        mcs = type(clsname, (_Unit, ), {})
        setattr(_this, clsname, mcs)
        for name, value in unitvalues.items():
            if hasattr(_this, name):
                raise Exception("Unable to create unit {} (dimension {}).".format(name, clsname))
            setattr(_this, name, mcs(name, (), {'_value': value, '_name': name}))


# Data order of isotopic (nuclear) properties:
_this = _sys.modules[__name__]
_path = _resource_filename("exa", "_static/units.json.bz2")
if not hasattr(_this, "s"):
    _create()
