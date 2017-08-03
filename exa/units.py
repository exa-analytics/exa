# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Units
############################
"""
import os as _os
import sys as _sys
from pkg_resources import resource_filename as _resource_filename
from exa import _jupyter_nbextension_paths
from .single import Singleton as _Singleton
from .core.editor import Editor as _Editor


_resource = "units.json.bz2"


class Unit(_Singleton):
    """A metaclass for creating units."""
    def __new__(mcs, name, bases, clsdict):
        #mcs.__repr__ = lambda self: repr(self.values)
        mcs.__repr__ = lambda self: "{}({}, {})".format(self.__class__.__name__, self._name, repr(self._value))
        return super(Unit, mcs).__new__(mcs, name, bases, clsdict)


def _create():
    """Generate the isotopes and elements API from their static data."""
    dct = _Editor(_path).to_data('json')
    for lclsname, unitvalues in dct.items():
        clsname = str(lclsname.title())
        mcs = type(clsname, (Unit, ), {})
        setattr(_this, clsname, mcs)
        for name, value in unitvalues.items():
            if hasattr(_this, name):
                raise Exception("Unable to create unit {} (dimension {}).".format(name, clsname))
            setattr(_this, str(name), mcs(str(name), (), {'_value': float(value), '_name': str(name)}))


# Data order of isotopic (nuclear) properties:
_this = _sys.modules[__name__]
_pkg = _jupyter_nbextension_paths()[0]['dest'].split("-")[1]
_static = _jupyter_nbextension_paths()[0]['src']
_path = _resource_filename(_pkg, _os.path.join(_static, _resource))
if not hasattr(_this, "s"):
    _create()
