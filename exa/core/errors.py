# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
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
