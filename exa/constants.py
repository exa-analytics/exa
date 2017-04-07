# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Physical Constants
#######################################
"""
import sys as _sys
from pkg_resources import resource_filename as _resource_filename
from .special import Singleton as _Singleton
from .core.editor import Editor as _Editor


class _Constant(_Singleton):
    """A metaclass for creating constants."""
    def __new__(mcs, name, bases, clsdict):
        mcs.__repr__ = lambda self: repr(self.value)
        return super(_Constant, mcs).__new__(mcs, name, bases, clsdict)


def _create():
    """Generate the isotopes and elements API from their static data."""
    lst = _Editor(_path).to_data('json')
    for entry in lst:
        name = str(entry['name'])
        setattr(_this, name, _Constant(name, (), entry))


# Data order of isotopic (nuclear) properties:
_this = _sys.modules[__name__]
_path = _resource_filename("exa", "data/constants.json.bz2")
if not hasattr(_this, "a220_lattice_spacing_of_silicon"):
    _create()
