# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Core Exceptions
#################################
"""
from exa.errors import ExaException


class UnitsError(ExaException):
    """
    Raised when attempting to add or subtract two objects with different units.
    """
    default = "Can't operate on objects with units {} and {}".format


class MissingUnits(ExaException):
    """Raised when attempting to convert units on a unitless object."""
    default = "Please set units on object: obj.units = exa.units.[unit]"
