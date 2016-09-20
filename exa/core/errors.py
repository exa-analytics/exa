# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Core Exceptions
#################################
"""
from exa.errors import ExaException


class AutomaticConversionError(ExaException):
    """
    Raised when a type conversion is attempted but fails.
    """
    fmt = 'Automatic type conversion to type {} failed for "{}" with type {}.'

    def __init__(self, obj, ptype):
        msg = self.fmt.format(obj.__class__.__name__, type(obj), ptype)
        super(AutomaticConversionError, self).__init__(msg, 'error')
