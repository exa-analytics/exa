# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Exceptions
#################################
This module provides the base exception class for exa specific exceptions.
"""
from exa._config import loggers


logger = loggers['sys']


class ExaException(Exception):
    """Generic exa exception/error."""
    def __init__(self, msg="default exception", level='info'):
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
