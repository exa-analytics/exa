# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Core Exceptions
#################################
Exceptions and errors raised by core objects.
"""
from exa.errors import ExaException


class UnitsError(ExaException):
    """Raised when operation cannot be performed due to units mismatch."""
    default = "Can't operate on objects with units {} and {}".format


class MissingUnits(ExaException):
    """Raised when attempting to convert units on a unitless object."""
    default = "Please set units on object: obj.units = exa.units.[unit]"


class NoParsers(ExaException):
    """Raised when a :class:`~exa.core.editor.Sections` object has no parsers."""
    default = "No parser objects have been added (see ``.add_section_parsers``)."

class NoSections(ExaException):
    """Raised when a :class:`~exa.core.editor.Sections` object has no sections."""
    default = "No sections have been defined or set (check ``.parse``)."
