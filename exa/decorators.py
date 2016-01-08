# -*- coding: utf-8 -*-
'''
Decorators
=====================
'''
from exa.log import get_logger


def logger(cls, log='system'):
    '''
    Instantiates a logger attribute on the class.
    '''
    cls._logger = get_logger(log)
    return cls
