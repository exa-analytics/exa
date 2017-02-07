# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Exceptions
#################################
This module provides the base exception class for exa specific exceptions.
"""
from exa._config import loggers


logger = loggers['sys']


class ExaException(Exception):
    """
    Exa exceptions allow for a default message. The message can be static or
    dynamic accepting both position and keyword arugments.
    """
    default = = None

    def __init__(self, *args, **kwargs):
        level = kwargs.pop('level', 'info')
        msg = kwargs.pop('msg', self.default)
        if callable(msg):
            msg = msg(*args, **kwargs)
        super(ExaException, self).__init__(msg)
        if level == 'info':
            logger.info(msg)
        elif level == 'warn':
            logger.warn(msg)
        elif level == 'error':
            logger.error(msg)
        elif level == 'critical':
            logger.critical(msg)
        else:
            logger.debug(msg)


class AutomaticConversionError(ExaException):
    """
    Raised when a type conversion is attempted but fails.

    See Also:
        :mod:`~exa.typed`.
    """
    default = 'Automatic type conversion to type {} failed for "{}" with type {}.'.format
