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
    fmt = "Can't add/subtract objects with units {} and {}".format

    def __init__(self, unit0, unit1):
        msg = self.fmt(unit0, unit1)
        super(UnitsError, self).__init__(msg, 'error')


class MissingUnits(ExaException):
    """Raised when attempting to convert units on a unitless object."""
    fmt = "Please set units on object: obj.units = exa.units.[unit]"

    def __init__(self):
        super(MissingUnits, self).__init__(self.fmt)
